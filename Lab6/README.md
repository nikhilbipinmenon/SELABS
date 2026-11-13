# Lab 6: Code and Branch Coverage Analysis

**Department of Computer Science and Engineering — PES University**  
**Course:** Software Engineering Laboratory (UE23CS252A)  

| Student Information | Details |
| :--- | :--- |
| **Student Name** | Nikhil B Menon |
| **SRN** | PES2UG24CS317 |
| **Section** | 5th Sem — Section F |
| **Assigned Scenario** | Problem Statement #10: Bus Transit Fare & Turnstile Monitoring (`bus_transit_fare.py`) |
| **Upstream Starter Repo** | [SETAPESU26/L6_L7_10_bus_transit_fare](https://github.com/SETAPESU26/L6_L7_10_bus_transit_fare) |

---

## 1. Executive Summary & Verification Highlights

| Metric Dimension | Initial Starter Test | Code Coverage Suite | Branch Coverage Suite | Department Target |
| :--- | :---: | :---: | :---: | :---: |
| **Test Case Count** | 1 test (100% pass) | 12 tests (100% pass) | 21 tests (100% pass) | Comprehensive Suite |
| **Line Coverage (%)** | **49%** (29 missed) | **100%** (0 missed) | **100%** (0 missed) | &ge; 90.0% |
| **Branch Coverage (%)** | **45%** (12 partial) | **100%** (0 partial) | **100%** (40/40 branches) | &ge; 90.0% |
| **Untested Paths** | Express fraud, senior/student, turnstile jams | None (57/57 stmts executed) | None (All 40 branches covered) | Zero unverified branches |

---

## 2. Deliverables in this Directory

| File / Folder | Description |
| :--- | :--- |
| **`PES2UG24CS317_Lab6.pdf`** | **Final Official Submission PDF** containing academic header, summary table, theoretical explanations, embedded terminal screenshots, and decision predicate traceability matrix. |
| **`bus_transit_fare.py`** | The module under test. |
| **`test_bus_transit.py`** | Baseline starter test from lab repository. |
| **`CodeCoverageTest_bus_transit_fare.py`** | Test suite achieving **100% Statement Coverage** (12 tests, 0 lines missed). |
| **`BranchCoverageTest_bus_transit_fare.py`** | Test suite achieving **100% Branch Coverage** (21 tests, 40/40 decision branches). |
| **`screenshots/`** | High-resolution terminal window captures for baseline and 100% test executions. |

---

## 3. Commands to Run (Quick Reference)

### 1. Install Testing Frameworks
```bash
pip install coverage pytest
```

### 2. Baseline Initial Coverage (Before Optimization)
```bash
# Baseline Line Coverage
python3 -m coverage run -m pytest test_bus_transit.py
python3 -m coverage report -m

# Baseline Branch Coverage
python3 -m coverage run --branch -m pytest test_bus_transit.py
python3 -m coverage report -m
```

### 3. Code Coverage Suite (100% Statement Coverage)
```bash
python3 -m coverage run -m pytest CodeCoverageTest_bus_transit_fare.py
python3 -m coverage report -m
```

### 4. Branch Coverage Suite (100% Decision Coverage)
```bash
python3 -m coverage run --branch -m pytest BranchCoverageTest_bus_transit_fare.py
python3 -m coverage report -m
```
