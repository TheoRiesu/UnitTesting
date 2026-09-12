# Simple CLI demo for clinic staff.
import sys
sys.path.insert(0, "src")

from clinic.service import ClinicService


def main():
    service = ClinicService()
    while True:
        print("\n--- Paws and Care ---")
        print("1. Register owner")
        print("2. View owners")
        print("3. Add pet (Dog/Cat/Bird/Rabbit)")
        print("4. View pets")
        print("5. Schedule appointment")
        print("6. View appointments")
        print("7. Cancel appointment")
        print("8. Update status")
        print("0. Exit")
        choice = input("Choice: ")

        try:
            if choice == "1":
                name = input("Name: ")
                contact = input("Contact: ")
                print("Registered:", service.register_owner(name, contact))
            elif choice == "2":
                for o in service.view_owners():
                    print(o)
            elif choice == "3":
                name = input("Pet name: ")
                ptype = input("Type (Dog/Cat/Bird/Rabbit): ")
                owner_id = input("Owner ID (e.g. O001): ")
                print("Added:", service.add_pet(name, ptype, owner_id))
            elif choice == "4":
                for p in service.view_pets():
                    print(p, "owner=" + p.owner_id)
            elif choice == "5":
                pet_id = input("Pet ID (e.g. P001): ")
                date_time = input("Date/time (e.g. 2026-09-20 10:30): ")
                reason = input("Reason: ")
                print("Scheduled:", service.schedule_appointment(pet_id, date_time, reason))
            elif choice == "6":
                for a in service.view_appointments():
                    print(a)
            elif choice == "7":
                appt_id = input("Appointment ID (e.g. A001): ")
                print("Cancelled:", service.cancel_appointment(appt_id))
            elif choice == "8":
                appt_id = input("Appointment ID: ")
                status = input("Status (Scheduled/Completed/Cancelled): ")
                print("Updated:", service.update_status(appt_id, status))
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Unknown choice")
        except ValueError as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
