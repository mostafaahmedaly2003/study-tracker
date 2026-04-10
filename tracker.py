#!/usr/bin/env python3
"""
Study Tracker CLI
Track your courses, log study sessions, and visualize your progress.

Usage:
  python tracker.py add       "Course Name" "Platform" <total_hours>
  python tracker.py log       "Course Name" <hours> ["optional note"]
  python tracker.py status
  python tracker.py today
  python tracker.py report
  python tracker.py list
  python tracker.py delete    "Course Name"
"""

import json
import sys
import os
from datetime import datetime, date, timedelta

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "study_data.json")


# ─────────────────────────── Data helpers ───────────────────────────

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"courses": {}, "sessions": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ─────────────────────────── Visual helpers ─────────────────────────

def progress_bar(percent, width=30):
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {percent:.1f}%"


def color(text, code):
    return f"\033[{code}m{text}\033[0m"


def green(t):  return color(t, "32")
def yellow(t): return color(t, "33")
def cyan(t):   return color(t, "36")
def bold(t):   return color(t, "1")
def dim(t):    return color(t, "2")


# ─────────────────────────── Commands ───────────────────────────────

def cmd_add(args):
    if len(args) < 3:
        print("Usage: python tracker.py add \"Course Name\" \"Platform\" <total_hours>")
        print("Example: python tracker.py add \"Python Bootcamp\" \"Udemy\" 40")
        return
    name, platform, total_hours = args[0], args[1], float(args[2])
    data = load_data()
    if name in data["courses"]:
        print(yellow(f'Course "{name}" already exists.'))
        return
    data["courses"][name] = {
        "platform":    platform,
        "total_hours": total_hours,
        "added_on":    str(date.today()),
        "completed":   False
    }
    save_data(data)
    print(green(f'Added: "{name}" ({platform}) — {total_hours}h total'))


def cmd_log(args):
    if len(args) < 2:
        print("Usage: python tracker.py log \"Course Name\" <hours> [\"note\"]")
        print("Example: python tracker.py log \"Python Bootcamp\" 1.5 \"Finished loops chapter\"")
        return
    name  = args[0]
    hours = float(args[1])
    note  = args[2] if len(args) > 2 else ""
    data  = load_data()
    if name not in data["courses"]:
        print(yellow(f'Course "{name}" not found. Add it first with: python tracker.py add'))
        return
    session = {
        "course": name,
        "hours":  hours,
        "note":   note,
        "date":   str(date.today()),
        "time":   datetime.now().strftime("%H:%M")
    }
    data["sessions"].append(session)
    # Check if completed
    logged = sum(s["hours"] for s in data["sessions"] if s["course"] == name)
    total  = data["courses"][name]["total_hours"]
    if logged >= total and not data["courses"][name]["completed"]:
        data["courses"][name]["completed"] = True
        print(green(f'Logged {hours}h for "{name}" — NOTE: logged {note}'))
        print(green(f'COMPLETED! You finished "{name}" after {logged:.1f}h'))
    else:
        pct = min(logged / total * 100, 100)
        print(green(f'Logged {hours}h for "{name}"'))
        print(f"  Progress: {progress_bar(pct)} ({logged:.1f}/{total}h)")
        if note:
            print(dim(f"  Note: {note}"))
    save_data(data)


def cmd_status(args):
    data = load_data()
    if not data["courses"]:
        print(yellow("No courses yet. Add one with: python tracker.py add"))
        return
    print(bold("\n─── Study Progress ───────────────────────────────────────"))
    total_logged = sum(s["hours"] for s in data["sessions"])
    print(f"  Total hours studied: {cyan(f'{total_logged:.1f}h')}\n")
    for name, info in sorted(data["courses"].items()):
        logged = sum(s["hours"] for s in data["sessions"] if s["course"] == name)
        total  = info["total_hours"]
        pct    = min(logged / total * 100, 100) if total > 0 else 0
        status = green("✅ DONE") if info.get("completed") else (
                 yellow("🔥 IN PROGRESS") if logged > 0 else dim("⬜ NOT STARTED"))
        print(f"  {bold(name)}")
        print(f"  {dim(info['platform'])} · {status}")
        print(f"  {progress_bar(pct)} ({logged:.1f}/{total}h)")
        print()
    print("─────────────────────────────────────────────────────────\n")


def cmd_today(args):
    data = load_data()
    today_str = str(date.today())
    sessions  = [s for s in data["sessions"] if s["date"] == today_str]
    if not sessions:
        print(yellow(f"No study sessions logged today ({today_str})."))
        return
    total = sum(s["hours"] for s in sessions)
    print(bold(f"\n─── Today ({today_str}) — {total:.1f}h total ───"))
    for s in sessions:
        note = f'  {dim(s["note"])}' if s["note"] else ""
        print(f"  {s['time']}  {cyan(s['course'])}  +{s['hours']}h{note}")
    print()


def cmd_report(args):
    data = load_data()
    today     = date.today()
    week_ago  = today - timedelta(days=6)
    print(bold(f"\n─── Weekly Report ({week_ago} → {today}) ──────────────"))
    weekly = {}
    for s in data["sessions"]:
        d = date.fromisoformat(s["date"])
        if week_ago <= d <= today:
            weekly[s["course"]] = weekly.get(s["course"], 0) + s["hours"]
    if not weekly:
        print(yellow("  No sessions this week.\n"))
        return
    week_total = sum(weekly.values())
    for course, hours in sorted(weekly.items(), key=lambda x: -x[1]):
        bar = "█" * int(hours * 4)
        print(f"  {cyan(course):<35} {hours:>5.1f}h  {bar}")
    print(f"\n  {bold('Total this week:')} {week_total:.1f}h")
    # Daily breakdown
    print(bold("\n─── Daily Breakdown ──────────────────────────────────────"))
    for i in range(7):
        day = week_ago + timedelta(days=i)
        day_hours = sum(s["hours"] for s in data["sessions"] if s["date"] == str(day))
        bar = "█" * int(day_hours * 4)
        label = "TODAY" if day == today else day.strftime("%a %d")
        print(f"  {label:<10} {day_hours:>4.1f}h  {bar}")
    print()


def cmd_list(args):
    data = load_data()
    if not data["courses"]:
        print(yellow("No courses added yet."))
        return
    print(bold("\n─── All Courses ──────────────────────────────────────────"))
    for name, info in sorted(data["courses"].items()):
        logged = sum(s["hours"] for s in data["sessions"] if s["course"] == name)
        done   = green("✅") if info.get("completed") else ("🔥" if logged > 0 else "⬜")
        print(f"  {done}  {name} ({info['platform']}) — {logged:.1f}/{info['total_hours']}h")
    print()


def cmd_delete(args):
    if not args:
        print("Usage: python tracker.py delete \"Course Name\"")
        return
    name = args[0]
    data = load_data()
    if name not in data["courses"]:
        print(yellow(f'Course "{name}" not found.'))
        return
    confirm = input(f'Delete "{name}" and all its sessions? (yes/no): ')
    if confirm.lower() == "yes":
        del data["courses"][name]
        data["sessions"] = [s for s in data["sessions"] if s["course"] != name]
        save_data(data)
        print(green(f'Deleted "{name}".'))
    else:
        print("Cancelled.")


def cmd_help(args):
    print(bold("\n─── Study Tracker ────────────────────────────────────────"))
    cmds = [
        ("add \"Name\" \"Platform\" <hours>", "Add a new course to track"),
        ("log \"Name\" <hours> [\"note\"]",   "Log a study session"),
        ("status",                            "Show progress for all courses"),
        ("today",                             "Show today's sessions"),
        ("report",                            "Show this week's report"),
        ("list",                              "List all courses"),
        ("delete \"Name\"",                   "Remove a course and its sessions"),
    ]
    for cmd, desc in cmds:
        print(f"  {cyan('python tracker.py ' + cmd)}")
        print(f"  {dim(desc)}\n")


# ─────────────────────────── Main ───────────────────────────────────

COMMANDS = {
    "add":    cmd_add,
    "log":    cmd_log,
    "status": cmd_status,
    "today":  cmd_today,
    "report": cmd_report,
    "list":   cmd_list,
    "delete": cmd_delete,
    "help":   cmd_help,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        cmd_help([])
    else:
        COMMANDS[sys.argv[1]](sys.argv[2:])
