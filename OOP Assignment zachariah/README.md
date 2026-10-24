# Patient Record System

**PROG211 Object-Oriented Programming 1 - Individual Assignment (Semester 03, Limkokwing University of Creative Technology, Sierra Leone)**
**Domain:** Health - Patient Record System

A small, menu-driven Python program that lets a clinic register patients, record visits, and review records, built with Object-Oriented Programming. It is designed as a **Digital Public Good (DPG)**: free, open, privacy-respecting and reusable by any clinic.

## Features
- Register patients using an anonymous ID (`PT-0001`, `PT-0002`, ...) and an optional alias
- Record a clinic visit with vital signs (temperature, pulse, blood pressure)
- Automatic alerts when vitals fall outside the normal range
- List, view, update and delete records
- Summary report by age group
- Input validation on every entry

## Project structure
| File | Purpose |
|---|---|
| `models.py` | The `Patient` and `Visit` classes |
| `records.py` | Functions to add, display, find, delete and summarise records (dictionary) |
| `main.py` | Menu and demo mode |

## How to run
Requires Python 3.8 or newer. No external libraries.

```bash
python main.py          # interactive menu
python main.py --demo   # automatic demonstration
```

## How it meets the assignment

| Requirement | Where |
|---|---|
| **Task 1** - two or more classes with attributes and methods | `Patient` and `Visit` in `models.py` (attributes such as `patient_id`, `age`, `vitals`; methods such as `display_info()`, `update_record()`) |
| Object creation and interaction | `Patient.add_visit(visit)` links a `Visit` object to a `Patient` object |
| **Task 2** - one data structure | A **dictionary** `{patient_id: Patient}` in `records.py`; `add_record()` and `display_records()` add and show records |
| Tuples (optional) | `Visit.vitals` is a tuple `(temp, pulse, systolic, diastolic)`; `NORMAL_RANGES`, `VALID_GENDERS` and `AGE_GROUPS` are constant tuples |
| **Task 3** - instance method | `Patient.add_visit()`, `Patient.update_record()`, `Visit.vitals_flags()` |
| Task 3 - class method | `Patient.generate_id()`, `Patient.total_registered()`, `Visit.total_recorded()` (all `@classmethod`) |
| Static method | `Patient.is_valid_age()`, `Visit.validate_vitals()` (both `@staticmethod`) |

## Alignment with Digital Public Goods (DPG) standards

1. **Open source** - the full source code is published in this public GitHub repository, so anyone can read, reuse and improve it.
2. **Inclusive and accessible design** - plain-language menu with numbered options, clear prompts, readable error messages, and no internet, account, or paid software needed. It runs on any computer with Python, including low-resource clinics.
3. **Privacy-respecting** - no real names, phone numbers, addresses or national IDs are collected. Patients are identified by an anonymous generated ID. Data is held only in memory while the program runs and is never written to disk or sent anywhere. Records can be deleted at any time (`Delete patient`).
4. **Modular and reusable** - the code is split into `models.py` (data and behaviour), `records.py` (storage) and `main.py` (user interface). Another clinic or developer can reuse the classes or replace the menu with a web or mobile front end without changing the models.

## Example usage (sample input and output)

**Input (interactive menu):**
```
Choose an option: 1
Alias / label (e.g. 'Patient A'): Patient D
Age: 25
Gender (Female/Male/Other): male
Clinic / ward: City Health Centre
```
**Output:**
```
Registered. Patient ID: PT-0001
```

**Input:**
```
Choose an option: 2
Patient ID: PT-0001
Reason for visit: Cough
Temperature (C): 37.2
Pulse (bpm): 78
Systolic BP: 120
Diastolic BP: 80
Diagnosis: Common cold
```
**Output:**
```
Visit recorded.
```

**Input:** `Choose an option: 3` then `Patient ID: pt-0001`
**Output:**
```
  Patient ID : PT-0001
  Alias      : Patient D
  Age        : 25 (Adult)
  Gender     : Male
  Clinic     : City Health Centre
  Visits     : 1
  Latest visit:
    Date      : 2026-10-16
    Reason    : Cough
    Vitals    : Temp 37.2 C | Pulse 78.0 bpm | BP 120.0/80.0
    Diagnosis : Common cold
    Alerts    : None - vitals normal
```

**Demo mode** (`python main.py --demo`) output, table section:
```
--------------------------------------------------------------------------
ID       Alias             Age   Gender   Clinic                Visits
--------------------------------------------------------------------------
PT-0001  Patient A         34    Female   Connaught Outpatient  1
PT-0002  Patient B         8     Male     Child Health Clinic   1
PT-0003  Patient C         67    Female   Elderly Care Ward     1
--------------------------------------------------------------------------
Total records: 3
```

## Design note
The assignment asks for **one** data structure, so patients are stored in a single dictionary keyed by patient ID (instant look-up). Each patient keeps its latest visit and a visit count, which keeps the program simple and focused on OOP.

## Licence
Released under the MIT Licence - free to use, copy and adapt.

## Author
Zachariah - Limkokwing University of Creative Technology, Sierra Leone
