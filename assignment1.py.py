import datetime

def welcome():
    print("="*45)
    print("\tWelcome to Your Daily Calorie Tracker!")
    print("="*45)
    print("Track your meals, see your total calories, check against your limit, and save your progress!")
    print("\nLet's make healthy choices together 🌱\n")

def get_meal_data():
    # Collect number of meals to log
    while True:
        try:
            num_meals = int(input("How many meals did you have today? "))
            if num_meals < 1:
                print("Enter at least 1 meal.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    meal_names, calorie_values = [], []
    for i in range(1, num_meals+1):
        meal = input(f"Enter name for meal #{i} (e.g., Breakfast, Lunch): ").strip()
        while True:
            try:
                calories = float(input(f"Enter calories for '{meal}': "))
                if calories < 0:
                    print("Calories can't be negative! Try again.")
                    continue
                break
            except ValueError:
                print("Please enter a number for calories (e.g., 350).")
        meal_names.append(meal)
        calorie_values.append(calories)
        print(f"Logged: {meal} = {calories} kcal\n")
    return meal_names, calorie_values

def calorie_stats(calorie_values):
    total = sum(calorie_values)
    avg = total / len(calorie_values) if calorie_values else 0
    return total, avg

def compare_limit(total):
    while True:
        try:
            daily_limit = float(input("Set your daily calorie limit (e.g., 2000): "))
            if daily_limit <= 0:
                print("Limit must be positive. Try again.")
                continue
            break
        except ValueError:
            print("Enter a number for the limit.")
    if total > daily_limit:
        message = f"🚨 Warning! You have exceeded your daily limit by {total - daily_limit:.2f} kcal."
    else:
        message = f"✅ Good job! You are within your daily calorie limit."
    return daily_limit, message

def print_summary(meal_names, calorie_values, total, avg, daily_limit, limit_message):
    print("\n" + "="*40)
    print("DAILY CALORIE INTAKE SUMMARY")
    print("="*40)
    print(f"{'Meal Name':<15}{'Calories (kcal)':>15}")
    print("-" * 30)
    for meal, cal in zip(meal_names, calorie_values):
        print(f"{meal:<15}\t{cal:>10.2f}")
    print("-" * 30)
    print(f"{'Total:':<15}\t{total:>10.2f}")
    print(f"{'Average:':<15}\t{avg:>10.2f}")
    print(f"{'Limit:':<15}\t{daily_limit:>10.2f}")
    print("\n" + limit_message)
    print("="*40 + "\n")

def save_log(meal_names, calorie_values, total, avg, daily_limit, limit_message):
    choice = input("Do you want to save this summary as a log file? (yes/no): ").strip().lower()
    if choice.startswith('y'):
        ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"calorie_log_{ts}.txt"
        try:
            with open(filename, "w") as f:
                f.write("Daily Calorie Tracker Log\n")
                f.write(f"Timestamp: {datetime.datetime.now()}\n\n")
                f.write(f"{'Meal Name':<15}{'Calories (kcal)':>15}\n")
                f.write("-" * 30 + "\n")
                for meal, cal in zip(meal_names, calorie_values):
                    f.write(f"{meal:<15}\t{cal:>10.2f}\n")
                f.write("-" * 30 + "\n")
                f.write(f"{'Total:':<15}\t{total:>10.2f}\n")
                f.write(f"{'Average:':<15}\t{avg:>10.2f}\n")
                f.write(f"{'Limit:':<15}\t{daily_limit:>10.2f}\n")
                f.write("\n" + limit_message + "\n")
            print(f"Session saved as '{filename}'. You can check this file later!")
        except Exception as e:
            print(f"Error saving file: {e}")
    else:
        print("Log not saved. You can run the program again anytime!")

def main():
    welcome()
    meal_names, calorie_values = get_meal_data()
    total, avg = calorie_stats(calorie_values)
    daily_limit, limit_message = compare_limit(total)
    print_summary(meal_names, calorie_values, total, avg, daily_limit, limit_message)
    save_log(meal_names, calorie_values, total, avg, daily_limit, limit_message)
    print("Thanks for tracking your day. Stay healthy! 💪")

if __name__ == "__main__":
    main()
