from datetime import datetime
from habits import (
    load_data, save_data, Habit, calculate_streak,
    get_longest_streak_for_habit, get_longest_streak_across_all, filter_by_periodicity
)

def print_table_header():
    print(f"\n{'ID':<5} | {'Habit Name':<22} | {'Periodicity':<12} | {'Current Streak':<15} | {'Max Historical':<15}")
    print("-" * 78)

def display_habit_row(habit, current_time):
    curr_streak = calculate_streak(habit.completion_history, habit.periodicity, current_time)
    max_streak = get_longest_streak_for_habit(habit)
    print(f"{habit.id:<5} | {habit.name:<22} | {habit.periodicity:<12} | {curr_streak:<15} | {max_streak:<15}")

def main():
    # Base fixed operational environment reference timeline set dynamically to mid-May 2026
    current_time = datetime(2026, 5, 17, 12, 0, 0)
    habits = load_data()

    print("======================================================")
    print("      WELCOME TO THE CLI HABIT TRACKER       ")
    print(f"      System Date: {current_time.date()}")
    print("======================================================")

    while True:
        print("\nCommands Available: [add] [remove] [mark] [check] [analyse] [exit]")
        cmd = input("Select an action > ").strip().lower()

        if cmd == "add":
            h_id = f"h{len(habits) + 1}"
            name = input("Enter habit name: ").strip()
            periodicity = ""
            while periodicity not in ["daily", "weekly"]:
                periodicity = input("Enter periodicity (daily/weekly): ").strip().lower()
            
            new_habit = Habit(h_id, name, periodicity, current_time.isoformat() + "Z")
            habits.append(new_habit)
            save_data(habits)
            print(f"Success: Added '{name}' under reference index ID: {h_id}")

        elif cmd == "remove":
            h_id = input("Enter the ID of the habit to remove: ").strip()
            initial_count = len(habits)
            habits = [h for h in habits if h.id != h_id]
            if len(habits) < initial_count:
                save_data(habits)
                print(f"Success: Removed habit with ID {h_id}.")
            else:
                print("Error: Habit ID not found.")

        elif cmd == "mark":
            h_id = input("Enter the Habit ID to complete: ").strip()
            found = False
            for h in habits:
                if h.id == h_id:
                    h.completion_history.append(current_time.isoformat() + "Z")
                    save_data(habits)
                    print(f"Registered check-off entry for '{h.name}' at {current_time.isoformat()}Z!")
                    found = True
                    break
            if not found:
                print("⚠ Error: Habit ID not found.")

        elif cmd == "check":
            if not habits:
                print("No habits tracked currently.")
                continue
            print_table_header()
            for h in habits:
                display_habit_row(h, current_time)

        elif cmd == "analyse":
            print("\n--- ANALYTICS ---")
            print("1. View longest tracking streak across all habits")
            print("2. Filter tracked elements by periodicity")
            choice = input("Select selection index (1 or 2): ").strip()
            
            if choice == "1":
                max_all = get_longest_streak_across_all(habits)
                print(f"\n» The longest unbroken historical streak across all tracked habits is: {max_all} periods.")
            elif choice == "2":
                p_filter = input("Enter periodicity filter target (daily/weekly): ").strip().lower()
                filtered = filter_by_periodicity(habits, p_filter)
                if not filtered:
                    print(f"No active tracking targets flagged as {p_filter}.")
                else:
                    print_table_header()
                    for h in filtered:
                        display_habit_row(h, current_time)
            else:
                print("Invalid input choice selected.")

        elif cmd == "exit":
            print("Exiting application execution safely. Goodbye!")
            break
        else:
            print("Error: Unknown command selection context.")

if __name__ == "__main__":
    main()