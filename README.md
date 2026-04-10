# Study Tracker CLI 📚

A zero-dependency Python CLI tool to track your courses, log study sessions, and visualize your weekly progress — all from the terminal.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/Dependencies-None_(stdlib_only)-brightgreen?style=flat)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

> Built as the Day 30 capstone project of the [30-Days-of-Python](https://github.com/mostafaahmedaly2003/30-days-of-python) challenge.

---

## Features

- Add courses with platform and total hours goal
- Log daily study sessions with optional notes
- Visual progress bars for every course
- Today's session summary
- 7-day weekly report with daily breakdown
- Zero external dependencies — pure Python stdlib

---

## Installation

```bash
git clone https://github.com/mostafaahmedaly2003/study-tracker.git
cd study-tracker
python tracker.py help
```

No `pip install` needed. Python 3.8+ only.

---

## Usage

```bash
# Add a course
python tracker.py add "Python Bootcamp" "Udemy" 40
python tracker.py add "CS50x" "edX" 60
python tracker.py add "ML Specialization" "Coursera" 90

# Log a study session
python tracker.py log "Python Bootcamp" 1.5 "Finished loops and functions"
python tracker.py log "CS50x" 2 "Problem Set 3 done"

# View progress for all courses
python tracker.py status

# See what you studied today
python tracker.py today

# Weekly report
python tracker.py report

# List all courses
python tracker.py list

# Delete a course
python tracker.py delete "Python Bootcamp"
```

---

## Example Output

### `python tracker.py status`

```
─── Study Progress ──────────────────────────────────

  Python Bootcamp
  Udemy · 🔥 IN PROGRESS
  [████████████░░░░░░░░░░░░░░░░░░] 40.0% (16.0/40h)

  CS50x
  edX · 🔥 IN PROGRESS
  [████████░░░░░░░░░░░░░░░░░░░░░░] 25.0% (15.0/60h)

  ML Specialization
  Coursera · ⬜ NOT STARTED
  [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0.0% (0.0/90h)
```

### `python tracker.py report`

```
─── Weekly Report (2026-04-05 → 2026-04-11) ──────────
  Python Bootcamp      8.0h  ████████████████████████████████
  CS50x                5.5h  ██████████████████████

  Total this week: 13.5h

─── Daily Breakdown ──────────────────────────────────
  Sat 05      1.5h  ██████
  Sun 06      2.0h  ████████
  Mon 07      0.0h
  Tue 08      3.0h  ████████████
  Wed 09      2.5h  ██████████
  Thu 10      1.5h  ██████
  TODAY       3.0h  ████████████
```

---

## Data Storage

Sessions are saved to `data/study_data.json` — plain JSON, human-readable, easy to back up.

```json
{
  "courses": {
    "Python Bootcamp": {
      "platform": "Udemy",
      "total_hours": 40,
      "added_on": "2026-04-11",
      "completed": false
    }
  },
  "sessions": [
    {
      "course": "Python Bootcamp",
      "hours": 1.5,
      "note": "Finished loops and functions",
      "date": "2026-04-11",
      "time": "20:30"
    }
  ]
}
```

---

## Author

**Mostafa Ahmed** — AI/ML Engineer  
[GitHub](https://github.com/mostafaahmedaly2003) · [LinkedIn](https://www.linkedin.com/in/mostafa-ahmed-ai/)
