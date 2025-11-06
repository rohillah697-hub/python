# gradebook.py
# Author: [Your Name]
# Date: 6th Oct, 2024
# Project Title: GradeBook Analyzer CLI

import csv
import statistics

def welcome():
    print("\n" + "=" * 45)
    print("👩‍🎓 GRADEBOOK ANALYZER: Analyze & Report Student Marks 👨‍🎓")
    print("=" * 45)
    print("Welcome! This tool helps you import student marks, calculate stats, assign grades, and generate summaries.\n")

def menu():
    print("MENU:")
    print("1. Manual Input (Type student names & marks)")
    print("2. Load from CSV file")
    print("3. Exit\n")

def get_manual_input():
    data = {}
    print("Manual Entry Mode – Enter names and marks (type 'done' when finished):")
    while True:
        name = input("Student name: ").strip()
        if name.lower() == 'done':
            break
        try:
            marks = float(input(f"Marks for {name}: "))
            if marks < 0 or marks > 100:
                print("Marks must be between 0 and 100.")
                continue
            data[name] = marks
        except ValueError:
            print("Please enter a valid number for marks.")
    return data

def get_csv_input():
    data = {}
    file = input("Enter CSV filename (e.g., students.csv): ").strip()
    try:
        with open(file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 2:
                    name = row[0].strip()
                    try:
                        marks = float(row[1])
                        data[name] = marks
                    except ValueError:
                        print(f"Skipping invalid entry for {name}.")
        print(f"Loaded {len(data)} records from {file}.")
    except Exception as e:
        print(f"Error loading file: {e}")
    return data

def calculate_average(marks_dict):
    return statistics.mean(marks_dict.values()) if marks_dict else 0

def calculate_median(marks_dict):
    return statistics.median(marks_dict.values()) if marks_dict else 0

def find_max_score(marks_dict):
    if not marks_dict:
        return None, None
    name = max(marks_dict, key=marks_dict.get)
    return name, marks_dict[name]

def find_min_score(marks_dict):
    if not marks_dict:
        return None, None
    name = min(marks_dict, key=marks_dict.get)
    return name, marks_dict[name]

def assign_grades(marks_dict):
    grades = {}
    for name, score in marks_dict.items():
        if score >= 90:
            grades[name] = 'A'
        elif score >= 80:
            grades[name] = 'B'
        elif score >= 70:
            grades[name] = 'C'
        elif score >= 60:
            grades[name] = 'D'
        else:
            grades[name] = 'F'
    return grades

def grade_distribution(grades):
    dist = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for g in grades.values():
        if g in dist:
            dist[g] += 1
    return dist

def pass_fail_lists(marks_dict):
    passed = [n for n, m in marks_dict.items() if m >= 40]
    failed = [n for n, m in marks_dict.items() if m < 40]
    return passed, failed

# ✅ Fixed function signature
def print_summary(marks_dict, grades, avg, median, max_info, min_info, dist, passed, failed):
    max_name, max_score = max_info
    min_name, min_score = min_info

    print("\n" + "=" * 45)
    print("GRADEBOOK SUMMARY")
    print("-" * 45)
    print(f"{'Name':<15}{'Marks':>8}{'Grade':>8}")
    print("-" * 36)
    for name in marks_dict:
        print(f"{name:<15}{marks_dict[name]:>8.2f}{grades[name]:>8}")
    print("-" * 36)
    print(f"{'Average':<15}{avg:>8.2f}")
    print(f"{'Median':<15}{median:>8.2f}")
    print(f"Topper: {max_name} ({max_score})")
    print(f"Lowest: {min_name} ({min_score})")
    print("-" * 36)
    for g in dist:
        print(f"Grade {g}: {dist[g]} student(s)")
    print(f"\nPass: {len(passed)} -> {', '.join(passed) if passed else 'None'}")
    print(f"Fail: {len(failed)} -> {', '.join(failed) if failed else 'None'}")
    print("=" * 45 + "\n")

def save_to_csv(marks_dict, grades):
    ans = input("Save results to CSV? (y/n): ").strip().lower()
    if ans.startswith('y'):
        fname = input("Enter filename (e.g., final_grades.csv): ").strip()
        try:
            with open(fname, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Marks', 'Grade'])
                for name in marks_dict:
                    writer.writerow([name, marks_dict[name], grades[name]])
            print(f"Results saved to {fname}")
        except Exception as e:
            print(f"Failed to save: {e}")

def main():
    welcome()
    while True:
        menu()
        choice = input("Choose an option (1/2/3): ").strip()
        marks_dict = {}

        if choice == '1':
            marks_dict = get_manual_input()
        elif choice == '2':
            marks_dict = get_csv_input()
        elif choice == '3':
            print("Thank you for using GradeBook Analyzer. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")
            continue

        if not marks_dict:
            print("No data found. Please try again.\n")
            continue

        # Statistical analysis
        avg = calculate_average(marks_dict)
        median = calculate_median(marks_dict)
        max_info = find_max_score(marks_dict)
        min_info = find_min_score(marks_dict)
        grades = assign_grades(marks_dict)
        dist = grade_distribution(grades)
        passed, failed = pass_fail_lists(marks_dict)

        # Results Table + Repetition Loop
        print_summary(marks_dict, grades, avg, median, max_info, min_info, dist, passed, failed)
        save_to_csv(marks_dict, grades)

        print("------ Analysis complete. ------\n")
        again = input("Analyze new data? (y/n): ").strip().lower()
        if not again.startswith('y'):
            print("Goodbye 👋")
            break

if __name__ == "__main__":
    main()
