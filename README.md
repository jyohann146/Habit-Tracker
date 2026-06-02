# Habit Tracker
This is a lightweight, zero-dependency, private command-line interface (CLI) habit tracking application built natively in Python. It utilizes an Object-Oriented background architecture alongside pure functional programming concepts to ensure seamless stability and tamper-proof streak calculations.

## Core Features
- **Strict Periodic Boundaries:** Supports separate calculation engines for Daily and Weekly habits.
- **Tamper-Proof Data Logging:** Records every check-off with absolute ISO-8601 timestamps inside a local JSON file instead of simple true/false checkboxes.
- **Pure Analytical Engine:** Math filters and streak counters run independently from storage, eliminating runtime database corruption risks.
- **Pre-Loaded Testing Data:** Starts with 4 weeks of baseline mock data to instantly demonstrate active streaks, misses, and recovery tracking.
- **Automated Quality Testing:** Features a complete unit-test powered by `pytest`.

## Installation & Setup
1. Ensure you have Python 3.0 installed on your machine.
2. Clone this repository or extract the project ZIP file into an empty directory.
3. Open a terminal windows inside the directory folder.

## How to Run the App
To start up your interactive terminal dashboard, execute:
```bash
python main.py
