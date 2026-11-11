# LAB 7: Fuzzing for Input Validation Bugs

**Student:** Nikhil B Menon  
**SRN:** PES2UG24CS317  
**Department:** Computer Science and Engineering, PES University  
**Topic:** Bus Transit Fare Calculator (`L6_L7_10_bus_transit_fare`)  
**Tools:** Python 3.8+, Hypothesis, Pytest

---

## Deliverables in this Directory

| File / Folder | Description |
| :--- | :--- |
| **`PES2UG24CS317_Lab7_FuzzTesting.pdf`** | **Final Submission PDF** containing all student details, lab steps, test results, code listings, and embedded terminal screenshots. |
| **`processor.py`** | **Fixed Application Script** hardened against all invalid inputs, nulls, edge cases, and division by zero. |
| **`test_processor.py`** | **Updated Test Script** utilizing Hypothesis `@given(st.text() \| st.none())` property-based fuzz testing. |
| **`processor_buggy.py`** | Original starter code preserved for reproduction of test failures. |
| **`screenshots/`** | High-resolution terminal screenshot captures for all lab steps (Steps 1, 2, 4, 5, and 6). |

---

## Commands to Run (Quick Reference)

### 1. Step 1: Install Dependencies
```bash
pip install hypothesis pytest
```

### 2. Step 2: Run Buggy Application
```bash
python processor_buggy.py
```
*Inputs to provide:*
- Corridor: `DT-UP-3`
- Category: `STUDENT`
- Density: `50/10.0`

### 3. Step 4: Run Fuzz Tests (Expose Failures)
To see the fuzz tests fail against the buggy code:
```bash
python -m pytest test_processor.py -v
```
*(When testing against `processor_buggy.py`)*

### 4. Step 5: Run Fixed Application
```bash
python processor.py
```
*Inputs to provide:*
- Corridor: `DT-UP-3`
- Category: `STUDENT`
- Density: `50/10.0`

### 5. Step 6: Run Fuzz Tests on Fixed Code (All Passed)
```bash
python -m pytest test_processor.py -v
```
*Result: 3 passed in <1s (100% success across hundreds of generated edge cases).*
