"""
main.py - Patient Record System (PROG211 Object-Oriented Programming 1)

Run:  python main.py          -> interactive menu
      python main.py --demo   -> automatic demonstration
"""

import sys

from models import Patient, Visit
from records import add_record, display_records, find_record, delete_record, summary_report


# ---------------------------------------------------------------- helpers
def read_int(prompt, low, high):
    while True:
        text = input(prompt).strip()
        if text.isdigit() and low <= int(text) <= high:
            return int(text)
        print(f"  Please enter a whole number from {low} to {high}.")


def read_float(prompt):
    while True:
        try:
            value = float(input(prompt).strip())
            if value > 0:
                return value
        except ValueError:
            pass
        print("  Please enter a positive number.")


def read_gender():
    options = "/".join(Patient.VALID_GENDERS)
    while True:
        value = input(f"Gender ({options}): ").strip().capitalize()
        if value in Patient.VALID_GENDERS:
            return value
        print("  Invalid choice.")


# ----------------------------------------------------------- menu actions
def register_patient(records):
    print("\n-- Register patient  --")
    alias = input("Alias / label (e.g. 'Patient A'): ")
    age = read_int("Age: ", Patient.MIN_AGE, Patient.MAX_AGE)
    gender = read_gender()
    clinic = input("Clinic / ward: ")
    patient = add_record(records, Patient(alias, age, gender, clinic))
    print(f"Registered. Patient ID: {patient.patient_id}")


def record_visit(records):
    patient = find_record(records, input("\nPatient ID: "))
    if patient is None:
        print("No such patient.")
        return
    reason = input("Reason for visit: ")
    temp = read_float("Temperature (C): ")
    pulse = read_float("Pulse (bpm): ")
    systolic = read_float("Systolic BP: ")
    diastolic = read_float("Diastolic BP: ")
    diagnosis = input("Diagnosis: ")
    patient.add_visit(Visit(reason, (temp, pulse, systolic, diastolic), diagnosis))
    print("Visit recorded.")


def view_patient(records):
    patient = find_record(records, input("\nPatient ID: "))
    if patient is None:
        print("No such patient.")
        return
    print()
    patient.display_info()


def update_patient(records):
    patient = find_record(records, input("\nPatient ID: "))
    if patient is None:
        print("No such patient.")
        return
    print("Leave a field blank to keep the current value.")
    alias = input(f"Alias [{patient.alias}]: ") or None
    age_text = input(f"Age [{patient.age}]: ").strip()
    clinic = input(f"Clinic [{patient.clinic}]: ") or None
    age = int(age_text) if age_text.isdigit() else None
    try:
        patient.update_record(alias=alias, age=age, clinic=clinic)
        print("Record updated.")
    except ValueError as error:
        print(f"Update failed: {error}")


def remove_patient(records):
    removed = delete_record(records, input("\nPatient ID to delete: "))
    print(f"{removed.patient_id} deleted." if removed else "No such patient.")


def menu(records):
    actions = {
        "1": register_patient, "2": record_visit, "3": view_patient,
        "4": display_records, "5": update_patient, "6": remove_patient,
        "7": summary_report,
    }
    while True:
        print("\n========== PATIENT RECORD SYSTEM ==========")
        print("1. Register patient      5. Update patient")
        print("2. Record a visit        6. Delete patient")
        print("3. View one patient      7. Summary report")
        print("4. List all patients     0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            return
        action = actions.get(choice)
        if action is None:
            print("Invalid option.")
        else:
            action(records)


# ------------------------------------------------------------------- demo
def run_demo(records):
    print("=== DEMO: creating patient objects ===")
    p1 = add_record(records, Patient("Patient A", 34, "Female", "Connaught Outpatient"))
    p2 = add_record(records, Patient("Patient B", 8, "Male", "Child Health Clinic"))
    p3 = add_record(records, Patient("Patient C", 67, "Female", "Elderly Care Ward"))
    print(f"Registered: {p1.patient_id}, {p2.patient_id}, {p3.patient_id}")

    print("\n=== DEMO: objects interacting (Visit linked to Patient) ===")
    p1.add_visit(Visit("Fever and headache", (38.9, 102, 118, 76), "Suspected malaria"))
    p2.add_visit(Visit("Routine check-up", (36.8, 88, 100, 65), "Healthy"))
    p3.add_visit(Visit("Dizziness", (36.6, 72, 165, 98), "High blood pressure"))
    p1.display_info()

    print("\n=== DEMO: all records (dictionary) ===")
    display_records(records)

    print("\n=== DEMO: instance method update_record() ===")
    p2.update_record(age=9)
    print(f"{p2.patient_id} age is now {p2.age} ({p2.age_group()})")

    print("\n=== DEMO: class methods and static method ===")
    print(f"Patient.total_registered() -> {Patient.total_registered()}")
    print(f"Visit.total_recorded()     -> {Visit.total_recorded()}")
    print(f"Patient.is_valid_age(150)  -> {Patient.is_valid_age(150)}")
    print(f"Visit.validate_vitals((37, 80, 120, 80)) -> {Visit.validate_vitals((37, 80, 120, 80))}")

    summary_report(records)

    print("\n=== DEMO: delete record (privacy - right to be forgotten) ===")
    delete_record(records, "PT-0002")
    display_records(records)


def main():
    records = {}  # the single data structure: dictionary keyed by patient ID
    if "--demo" in sys.argv:
        run_demo(records)
    else:
        menu(records)


if __name__ == "__main__":
    main()
