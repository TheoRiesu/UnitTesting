import os
import sqlite3
from pathlib import Path

from .models import Owner, Appointment
from .factory import PetFactory


def _default_db_path():
    if os.environ.get("CLINIC_DB_PATH"):
        return Path(os.environ["CLINIC_DB_PATH"])
    # .../UnitTesting/data/data.db (repo root = parents[2] of this file)
    return Path(__file__).resolve().parents[2] / "data" / "data.db"


class ClinicDatabase:
    _instance = None
    _custom_path = None

    def __new__(cls, db_path=None):
        if cls._instance is None:
            inst = super().__new__(cls)
            inst.owners = {}
            inst.pets = {}
            inst.appointments = {}
            inst.owner_seq = 0
            inst.pet_seq = 0
            inst.appointment_seq = 0
            inst._db_path = Path(db_path or cls._custom_path or _default_db_path())
            inst._db_path.parent.mkdir(parents=True, exist_ok=True)
            inst._conn = sqlite3.connect(str(inst._db_path))
            inst._conn.row_factory = sqlite3.Row
            inst._init_schema()
            inst._load()
            cls._instance = inst
        return cls._instance

    @classmethod
    def get_instance(cls, db_path=None):
        if db_path is not None and cls._instance is not None:
            if Path(db_path) != cls._instance._db_path:
                cls.reset_instance()
        return cls(db_path=db_path)

    @classmethod
    def configure(cls, db_path=None):
        """Point next instance at a different file (tests). None = default."""
        cls._custom_path = str(db_path) if db_path else None
        cls.reset_instance()

    @classmethod
    def reset_instance(cls):
        """Drop singleton (simulates process restart). Next get_instance() reloads from file."""
        if cls._instance is not None:
            try:
                cls._instance._conn.commit()
                cls._instance._conn.close()
            except Exception:
                pass
            cls._instance = None

    def _init_schema(self):
        c = self._conn
        c.execute("PRAGMA journal_mode=WAL;")
        c.execute("PRAGMA foreign_keys=ON;")
        c.execute(
            "CREATE TABLE IF NOT EXISTS owners("
            " owner_id TEXT PRIMARY KEY, name TEXT NOT NULL,"
            " contact_number TEXT NOT NULL)"
        )
        c.execute(
            "CREATE TABLE IF NOT EXISTS pets("
            " pet_id TEXT PRIMARY KEY, name TEXT NOT NULL,"
            " owner_id TEXT NOT NULL REFERENCES owners(owner_id),"
            " age INTEGER NOT NULL DEFAULT 0, species TEXT NOT NULL)"
        )
        c.execute(
            "CREATE TABLE IF NOT EXISTS appointments("
            " appointment_id TEXT PRIMARY KEY, pet_id TEXT NOT NULL"
            " REFERENCES pets(pet_id), owner_id TEXT NOT NULL,"
            " date_time TEXT NOT NULL, reason TEXT NOT NULL DEFAULT '',"
            " status TEXT NOT NULL DEFAULT 'Scheduled')"
        )
        c.execute(
            "CREATE TABLE IF NOT EXISTS counters("
            " name TEXT PRIMARY KEY, value INTEGER NOT NULL)"
        )
        for name in ("owner", "pet", "appointment"):
            c.execute(
                "INSERT OR IGNORE INTO counters(name, value) VALUES(?, 0)", (name,)
            )
        self._conn.commit()

    def _load(self):
        c = self._conn
        self.owners = {}
        for r in c.execute("SELECT owner_id, name, contact_number FROM owners"):
            self.owners[r["owner_id"]] = Owner(
                r["owner_id"], r["name"], r["contact_number"]
            )
        self.pets = {}
        for r in c.execute(
            "SELECT pet_id, name, owner_id, age, species FROM pets"
        ):
            try:
                pet = PetFactory.create_pet(
                    r["species"], r["pet_id"], r["name"], r["owner_id"], r["age"]
                )
            except ValueError:
                continue
            self.pets[r["pet_id"]] = pet
        self.appointments = {}
        for r in c.execute(
            "SELECT appointment_id, pet_id, owner_id, date_time, reason, status"
            " FROM appointments"
        ):
            appt = Appointment(
                r["appointment_id"], r["pet_id"], r["owner_id"],
                r["date_time"], r["reason"],
            )
            appt.status = r["status"]
            self.appointments[r["appointment_id"]] = appt
        self.owner_seq = self._counter("owner", "O")
        self.pet_seq = self._counter("pet", "P")
        self.appointment_seq = self._counter("appointment", "A")

    def _counter(self, name, prefix):
        row = self._conn.execute(
            "SELECT value FROM counters WHERE name=?", (name,)
        ).fetchone()
        try:
            stored = int(row["value"]) if row else 0
        except (TypeError, ValueError):
            stored = 0
        table, col = {
            "owner": ("owners", "owner_id"),
            "pet": ("pets", "pet_id"),
            "appointment": ("appointments", "appointment_id"),
        }[name]
        max_seen = 0
        for (raw_id,) in self._conn.execute(f"SELECT {col} FROM {table}"):
            try:
                if raw_id and raw_id.startswith(prefix):
                    max_seen = max(max_seen, int(raw_id[len(prefix):]))
            except ValueError:
                continue
        value = max(stored, max_seen)
        self._conn.execute(
            "UPDATE counters SET value=? WHERE name=?", (value, name)
        )
        self._conn.commit()
        return value

    def _bump_counter(self, name):
        value = self._counter(name, {"owner": "O", "pet": "P", "appointment": "A"}[name]) + 1
        self._conn.execute(
            "UPDATE counters SET value=? WHERE name=?", (value, name)
        )
        self._conn.commit()
        return value

    def next_owner_id(self):
        self.owner_seq = self._bump_counter("owner")
        return "O" + str(self.owner_seq).zfill(3)

    def next_pet_id(self):
        self.pet_seq = self._bump_counter("pet")
        return "P" + str(self.pet_seq).zfill(3)

    def next_appointment_id(self):
        self.appointment_seq = self._bump_counter("appointment")
        return "A" + str(self.appointment_seq).zfill(3)

    def save_owner(self, owner):
        self.owners[owner.owner_id] = owner
        self._conn.execute(
            "INSERT OR REPLACE INTO owners(owner_id, name, contact_number)"
            " VALUES(?, ?, ?)",
            (owner.owner_id, owner.name, owner.contact_number),
        )
        self._conn.commit()
        return owner

    def save_pet(self, pet):
        self.pets[pet.pet_id] = pet
        self._conn.execute(
            "INSERT OR REPLACE INTO pets(pet_id, name, owner_id, age, species)"
            " VALUES(?, ?, ?, ?, ?)",
            (pet.pet_id, pet.name, pet.owner_id, pet.age, pet.species),
        )
        self._conn.commit()
        return pet

    def save_appointment(self, appt):
        self.appointments[appt.appointment_id] = appt
        self._conn.execute(
            "INSERT OR REPLACE INTO appointments"
            "(appointment_id, pet_id, owner_id, date_time, reason, status)"
            " VALUES(?, ?, ?, ?, ?, ?)",
            (
                appt.appointment_id, appt.pet_id, appt.owner_id,
                appt.date_time, appt.reason, appt.status,
            ),
        )
        self._conn.commit()
        return appt

    def clear(self):
        self._conn.execute("DELETE FROM appointments")
        self._conn.execute("DELETE FROM pets")
        self._conn.execute("DELETE FROM owners")
        self._conn.execute("UPDATE counters SET value=0")
        self._conn.commit()
        self.owners = {}
        self.pets = {}
        self.appointments = {}
        self.owner_seq = 0
        self.pet_seq = 0
        self.appointment_seq = 0

    def close(self):
        try:
            self._conn.commit()
            self._conn.close()
        except Exception:
            pass
