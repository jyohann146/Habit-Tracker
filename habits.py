import json
import os
from datetime import datetime, timedelta

class Habit:
    def __init__(self, habit_id, name, periodicity, creation_date, completion_history=None):
        self.id = habit_id
        self.name = name
        self.periodicity = periodicity.lower()  # "daily" or "weekly"
        self.creation_date = creation_date
        self.completion_history = completion_history if completion_history else []

    def to_dict(self):
        """Serializes the habit instance to a dictionary for JSON storage."""
        return {
            "id": self.id,
            "name": self.name,
            "periodicity": self.periodicity,
            "creation_date": self.creation_date,
            "completion_history": self.completion_history
        }
# PURE FUNCTIONAL ANALYTICS ENGINE

def get_all_habits(habits_data):
    """Pure function returning all habit names/IDs."""
    return [habit.name for habit in habits_data]


def filter_by_periodicity(habits_data, periodicity):
    """Pure function returning habits filtered by daily or weekly criteria."""
    target = periodicity.lower()
    return [h for h in habits_data if h.periodicity == target]


def calculate_streak(completion_history, periodicity, current_date=None):
    """
    Pure function to calculate the current or historical longest streak.
    If current_date is provided, it calculates the 'current active streak'.
    Otherwise, it determines the 'longest historical streak' ever recorded.
    """
    if not completion_history:
        return 0

    # Parse timestamps and sort them chronologically
    dates = sorted(list(set([datetime.fromisoformat(t.replace("Z", "+00:00")).date() for t in completion_history])))
    
    if periodicity == "daily":
        # Calculate longest historical daily streak
        longest_streak = 0
        current_streak = 0
        prev_date = None

        for d in dates:
            if prev_date is None:
                current_streak = 1
            elif (d - prev_date).days == 1:
                current_streak += 1
            elif (d - prev_date).days > 1:
                if current_streak > longest_streak:
                    longest_streak = current_streak
                current_streak = 1
            prev_date = d
        
        longest_streak = max(longest_streak, current_streak)

        # Check if the streak is currently broken relative to an absolute tracking date
        if current_date:
            today = current_date.date()
            if dates[-1] == today:
                return current_streak
            elif dates[-1] == today - timedelta(days=1):
                return current_streak
            else:
                return 0  # Streak is broken
        return longest_streak

    elif periodicity == "weekly":
        # Calculate weekly streaks based on ISO calendar week numbers
        # An event counts once per ISO week (year, week_num)
        weeks = sorted(list(set([(d.isocalendar()[0], d.isocalendar()[1]) for d in dates])))
        
        longest_streak = 0
        current_streak = 0
        prev_week_coords = None

        for w in weeks:
            if prev_week_coords is None:
                current_streak = 1
            else:
                # Calculate week difference cleanly
                prev_date_obj = datetime.fromisocalendar(prev_week_coords[0], prev_week_coords[1], 1)
                curr_date_obj = datetime.fromisocalendar(w[0], w[1], 1)
                week_diff = round((curr_date_obj - prev_date_obj).days / 7)
                
                if week_diff == 1:
                    current_streak += 1
                elif week_diff > 1:
                    if current_streak > longest_streak:
                        longest_streak = current_streak
                    current_streak = 1
            prev_week_coords = w
            
        longest_streak = max(longest_streak, current_streak)

        if current_date:
            curr_year, curr_wk, _ = current_date.isocalendar()
            last_recorded_wk = weeks[-1]
            last_date_obj = datetime.fromisocalendar(last_recorded_wk[0], last_recorded_wk[1], 1)
            today_date_obj = datetime.fromisocalendar(curr_year, curr_wk, 1)
            week_diff = round((today_date_obj - last_date_obj).days / 7)
            
            if week_diff <= 1:
                return current_streak
            else:
                return 0 # Streak broken
        return longest_streak


def get_longest_streak_for_habit(habit):
    """Pure function calculating the maximum historical streak for a single habit."""
    return calculate_streak(habit.completion_history, habit.periodicity, current_date=None)


def get_longest_streak_across_all(habits_data):
    """Pure function evaluating max historical streak across all tracked habits."""
    if not habits_data:
        return 0
    return max([get_longest_streak_for_habit(h) for h in habits_data])

# FILE DATA MANAGEMENT SYSTEM

def get_mock_data():
    """Generates 4 weeks of baseline mock data ending near mid-May 2026."""
    base_date = datetime(2026, 4, 19, 12, 0, 0)
    
    # h1: Perfect Daily (28 Days)
    h1_history = [(base_date + timedelta(days=i)).isoformat() + "Z" for i in range(28)]
    
    # h2: Daily with a break in Week 2 (days 10 and 11 skipped)
    h2_history = []
    for i in range(28):
        if i not in [10, 11]:
            h2_history.append((base_date + timedelta(days=i)).isoformat() + "Z")
            
    # h3: Daily started 2 weeks late (only last 14 days)
    h3_history = [(base_date + timedelta(days=i)).isoformat() + "Z" for i in range(14, 28)]
    
    # h4: Perfect Weekly (4 Weeks)
    h4_history = [
        (base_date + timedelta(days=2)).isoformat() + "Z",  # Week 1
        (base_date + timedelta(days=9)).isoformat() + "Z",  # Week 2
        (base_date + timedelta(days=16)).isoformat() + "Z", # Week 3
        (base_date + timedelta(days=23)).isoformat() + "Z"  # Week 4
    ]
    
    # h5: Weekly missed during Week 3
    h5_history = [
        (base_date + timedelta(days=2)).isoformat() + "Z",  # Week 1
        (base_date + timedelta(days=9)).isoformat() + "Z",  # Week 2
        # Week 3 skipped completely
        (base_date + timedelta(days=23)).isoformat() + "Z"  # Week 4
    ]

    return {
        "meta": {"system_initialized": base_date.isoformat() + "Z"},
        "habits": [
            {"id": "h1", "name": "Daily Reading", "periodicity": "daily", "creation_date": base_date.isoformat() + "Z", "completion_history": h1_history},
            {"id": "h2", "name": "Hydration Target", "periodicity": "daily", "creation_date": base_date.isoformat() + "Z", "completion_history": h2_history},
            {"id": "h3", "name": "Morning Gym", "periodicity": "daily", "creation_date": base_date.isoformat() + "Z", "completion_history": h3_history},
            {"id": "h4", "name": "Weekly House Clean", "periodicity": "weekly", "creation_date": base_date.isoformat() + "Z", "completion_history": h4_history},
            {"id": "h5", "name": "Weekly Review", "periodicity": "weekly", "creation_date": base_date.isoformat() + "Z", "completion_history": h5_history}
        ]
    }


def load_data(filepath="data.json"):
    # If the file does not exist, build the mock data dictionary structure
    if not os.path.exists(filepath):
        mock_payload = get_mock_data()
        
        # Convert the raw dictionaries from get_mock_data() into internal Habit objects
        habits = []
        for item in mock_payload["habits"]:
            habits.append(Habit(
                item["id"], 
                item["name"], 
                item["periodicity"], 
                item["creation_date"], 
                item["completion_history"]
            ))
        
        # Save them correctly as a clean array to disk
        save_data(habits, filepath)
        return habits

    # If the file DOES exist, read it safely
    with open(filepath, "r") as f:
        data = json.load(f)
        
    habits = []
    
    # Safely digest whatever structural format is currently in data.json
    if "habits" in data:
        if isinstance(data["habits"], list):
            for item in data["habits"]:
                if isinstance(item, dict):
                    habits.append(Habit(
                        item.get("id", ""), 
                        item.get("name", ""), 
                        item.get("periodicity", "daily"), 
                        item.get("creation_date", ""), 
                        item.get("completion_history", [])
                    ))
        elif isinstance(data["habits"], dict):
            for habit_id, details in data["habits"].items():
                if isinstance(details, dict):
                    habits.append(Habit(
                        habit_id, 
                        details.get("name", ""), 
                        details.get("periodicity", "daily"), 
                        details.get("creation_date", ""), 
                        details.get("completion_history", [])
                    ))
                    
    # Fallback safety: If data became corrupted or empty inside, rebuild mock entries
    if not habits:
        print("⚠ Habit tracking data container empty. Re-seeding baseline 4-week dataset...")
        mock_payload = get_mock_data()
        for item in mock_payload["habits"]:
            habits.append(Habit(item["id"], item["name"], item["periodicity"], item["creation_date"], item["completion_history"]))
        save_data(habits, filepath)

    return habits


def save_data(habits_list, filepath="data.json"):
    raw_list = []
    for h in habits_list:
        if isinstance(h, Habit):
            raw_list.append(h.to_dict())
        elif isinstance(h, dict):
            raw_list.append(h)
            
    payload = {
        "meta": {"system_initialized": datetime.now().isoformat() + "Z"},
        "habits": raw_list
    }
    with open(filepath, "w") as f:
        json.dump(payload, f, indent=2)
