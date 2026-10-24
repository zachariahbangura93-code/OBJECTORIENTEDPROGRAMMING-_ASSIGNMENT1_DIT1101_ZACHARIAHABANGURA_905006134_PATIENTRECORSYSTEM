"""
records.py - Storage and retrieval of patient records.

The ONE data structure used by the program is a dictionary:
    { patient_id (str) : Patient object }
The patient's unique ID is the key, so look-ups are instant.
"""

from models import Patient


def add_record(records, patient):
    """Add a Patient to the records dictionary."""
    if patient.patient_id in records:
        raise ValueError(f"{patient.patient_id} already exists")
    records[patient.patient_id] = patient
    return patient


def display_records(records):
    """Print every patient in a table."""
    if not records:
        print("\nNo patient records yet.")
        return
    line = "-" * 74
    print(f"\n{line}")
    print(f"{'ID':<9}{'Alias':<18}{'Age':<6}{'Gender':<9}{'Clinic':<22}{'Visits':<6}")
    print(line)
    for patient_id, patient in records.items():
        print(f"{patient_id:<9}{patient.alias:<18}{patient.age:<6}"
              f"{patient.gender:<9}{patient.clinic:<22}{patient.visit_count:<6}")
    print(line)
    print(f"Total records: {len(records)}")


def find_record(records, patient_id):
    """Return the Patient with this ID, or None."""
    return records.get(patient_id.strip().upper())


def delete_record(records, patient_id):
    """Remove a record (supports the patient's right to be forgotten)."""
    return records.pop(patient_id.strip().upper(), None)


def summary_report(records):
    """Print a count of patients per age group and visits needing attention."""
    print("\n=== SUMMARY REPORT ===")
    print(f"Patients on file        : {len(records)}")
    for group in Patient.AGE_GROUPS:
        count = sum(1 for p in records.values() if p.age_group() == group)
        print(f"  {group:<14}: {count}")
    alerts = [p.patient_id for p in records.values()
              if p.latest_visit and p.latest_visit.vitals_flags()]
    print(f"Latest visit has alerts : {', '.join(alerts) if alerts else 'none'}")
