"""
models.py - Domain classes for the Patient Record System.

Privacy by design (Digital Public Goods principle): no real names, phone
numbers, addresses or national IDs are stored. Each patient is identified by
an auto-generated anonymous ID and an optional alias chosen by the clinic.
"""

from datetime import date


class Visit:
    """A single clinic visit. Vital signs are kept in an immutable tuple."""

    # Tuple of (label, lowest normal, highest normal) - fixed, so a tuple fits.
    NORMAL_RANGES = (
        ("Temperature (C)", 36.0, 37.5),
        ("Pulse (bpm)", 60, 100),
        ("Systolic BP", 90, 140),
        ("Diastolic BP", 60, 90),
    )

    total_visits = 0  # class attribute shared by every Visit object

    def __init__(self, reason, vitals, diagnosis, visit_date=None):
        if not Visit.validate_vitals(vitals):
            raise ValueError(
                "Vitals must be 4 positive numbers: "
                "(temperature, pulse, systolic, diastolic)"
            )
        self.reason = reason.strip()
        self.vitals = tuple(vitals)          # (temp, pulse, systolic, diastolic)
        self.diagnosis = diagnosis.strip()
        self.visit_date = visit_date or date.today().isoformat()
        self.patient_id = None               # set when linked to a Patient
        Visit.total_visits += 1

    # ---- static method: no access to the object or class needed ----
    @staticmethod
    def validate_vitals(vitals):
        """Return True if vitals is a 4-item tuple/list of positive numbers."""
        if not isinstance(vitals, (tuple, list)) or len(vitals) != 4:
            return False
        return all(isinstance(v, (int, float)) and v > 0 for v in vitals)

    # ---- class method: works with class-level data ----
    @classmethod
    def total_recorded(cls):
        """Return how many Visit objects have been created."""
        return cls.total_visits

    # ---- instance methods ----
    def vitals_flags(self):
        """Return a list of warnings for vitals outside the normal range."""
        flags = []
        for (label, low, high), value in zip(Visit.NORMAL_RANGES, self.vitals):
            if value < low:
                flags.append(f"{label} LOW ({value})")
            elif value > high:
                flags.append(f"{label} HIGH ({value})")
        return flags

    def display_info(self):
        temp, pulse, systolic, diastolic = self.vitals
        print(f"    Date      : {self.visit_date}")
        print(f"    Reason    : {self.reason}")
        print(f"    Vitals    : Temp {temp} C | Pulse {pulse} bpm | BP {systolic}/{diastolic}")
        print(f"    Diagnosis : {self.diagnosis}")
        flags = self.vitals_flags()
        print(f"    Alerts    : {', '.join(flags) if flags else 'None - vitals normal'}")


class Patient:
    """An anonymised patient record."""

    VALID_GENDERS = ("Female", "Male", "Other")
    AGE_GROUPS = ("Child", "Adolescent", "Adult", "Older adult")
    MIN_AGE, MAX_AGE = 0, 120

    _count = 0  # class attribute used to generate unique IDs

    def __init__(self, alias, age, gender, clinic):
        if not Patient.is_valid_age(age):
            raise ValueError(f"Age must be a whole number from {Patient.MIN_AGE} to {Patient.MAX_AGE}")
        if gender not in Patient.VALID_GENDERS:
            raise ValueError(f"Gender must be one of {Patient.VALID_GENDERS}")
        self.patient_id = Patient.generate_id()
        self.alias = alias.strip() or "Unnamed"
        self.age = age
        self.gender = gender
        self.clinic = clinic.strip()
        self.latest_visit = None   # a Visit object (object interaction)
        self.visit_count = 0

    # ---- class methods ----
    @classmethod
    def generate_id(cls):
        """Create the next anonymous ID, e.g. PT-0001."""
        cls._count += 1
        return f"PT-{cls._count:04d}"

    @classmethod
    def total_registered(cls):
        """Return how many patients have been registered this session."""
        return cls._count

    # ---- static method ----
    @staticmethod
    def is_valid_age(age):
        return isinstance(age, int) and Patient.MIN_AGE <= age <= Patient.MAX_AGE

    # ---- instance methods ----
    def age_group(self):
        if self.age < 13:
            return Patient.AGE_GROUPS[0]
        if self.age < 20:
            return Patient.AGE_GROUPS[1]
        if self.age < 60:
            return Patient.AGE_GROUPS[2]
        return Patient.AGE_GROUPS[3]

    def add_visit(self, visit):
        """Link a Visit object to this patient (interaction between objects)."""
        visit.patient_id = self.patient_id
        self.latest_visit = visit
        self.visit_count += 1

    def update_record(self, alias=None, age=None, clinic=None):
        """Update only the fields that are provided."""
        if age is not None:
            if not Patient.is_valid_age(age):
                raise ValueError("Invalid age")
            self.age = age
        if alias is not None:
            self.alias = alias.strip() or self.alias
        if clinic is not None:
            self.clinic = clinic.strip() or self.clinic

    def display_info(self):
        print(f"  Patient ID : {self.patient_id}")
        print(f"  Alias      : {self.alias}")
        print(f"  Age        : {self.age} ({self.age_group()})")
        print(f"  Gender     : {self.gender}")
        print(f"  Clinic     : {self.clinic}")
        print(f"  Visits     : {self.visit_count}")
        if self.latest_visit:
            print("  Latest visit:")
            self.latest_visit.display_info()
        else:
            print("  Latest visit: none recorded")
