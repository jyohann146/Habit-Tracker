import pytest
from datetime import datetime, timedelta
from habits import Habit, calculate_streak, get_longest_streak_for_habit, get_longest_streak_across_all

def test_daily_streak_calculation():
    # Setup perfect continuous 5-day daily tracker history profiles
    base = datetime(2026, 5, 1, 10, 0, 0)
    history = [(base + timedelta(days=i)).isoformat() + "Z" for i in range(5)]
    
    habit = Habit("t1", "Test Coding", "daily", base.isoformat() + "Z", history)
    
    # Max historical sequence length query tracking validation checks
    assert get_longest_streak_for_habit(habit) == 5
    
    # Active execution parameter evaluation window contexts (Evaluate precisely on final sequence point)
    eval_time = base + timedelta(days=4)
    assert calculate_streak(habit.completion_history, "daily", current_date=eval_time) == 5

def test_broken_daily_streak():
    # Setup history sequence with an absolute gap on Day 4
    base = datetime(2026, 5, 1, 10, 0, 0)
    history = [
        (base + timedelta(days=0)).isoformat() + "Z",
        (base + timedelta(days=1)).isoformat() + "Z",
        (base + timedelta(days=2)).isoformat() + "Z",
        # Day 3 skipped
        (base + timedelta(days=4)).isoformat() + "Z",
        (base + timedelta(days=5)).isoformat() + "Z",
    ]
    habit = Habit("t2", "Water Plants", "daily", base.isoformat() + "Z", history)
    
    # Longest historical cluster logic check (the initial 3-day run)
    assert get_longest_streak_for_habit(habit) == 3
    
    # Ensure current evaluation relative to a late date correctly marks active streak as broken (0)
    eval_late = base + timedelta(days=10)
    assert calculate_streak(habit.completion_history, "daily", current_date=eval_late) == 0

def test_weekly_streak_calculation():
    # 3 continuous ISO-week completions setup configuration profile tracks
    base = datetime(2026, 5, 1, 12, 0, 0) # Week 18
    history = [
        (base).isoformat() + "Z",                           # Week 18
        (base + timedelta(days=7)).isoformat() + "Z",        # Week 19
        (base + timedelta(days=14)).isoformat() + "Z",       # Week 20
    ]
    habit = Habit("t3", "Weekly Cleaning Run", "weekly", base.isoformat() + "Z", history)
    
    assert get_longest_streak_for_habit(habit) == 3

def test_longest_streak_across_all():
    base = datetime(2026, 5, 1, 12, 0, 0)
    h1 = Habit("t1", "Habit A", "daily", base.isoformat() + "Z", [(base + timedelta(days=i)).isoformat() + "Z" for i in range(10)]) # Streak 10
    h2 = Habit("t2", "Habit B", "daily", base.isoformat() + "Z", [(base + timedelta(days=i)).isoformat() + "Z" for i in range(4)])  # Streak 4
    
    assert get_longest_streak_across_all([h1, h2]) == 10