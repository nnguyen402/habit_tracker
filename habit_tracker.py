import json
from datetime import datetime, timedelta
import os
from tabulate import tabulate


# 1: Json file methods

file_path = "data/habits.json"
def load_data(filepath): 
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)
    else:
        intialize_json(filepath)
        return {}

def save_data(data, filepath):
    if os.path.exists(filepath):
        with open(filepath, 'w') as file:
            return json.dump(data, file, indent = 2)
    return {}

def intialize_json(filepath):
    data = {}
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=2)
# ------------------------------------------- #


def add_category(habit_name, data):
    if (habit_name in data):
        print("Habit already exists")
        return
    if habit_name == "":
        print("Enter valid name")
        return
    data[habit_name] = {}

    save_data(data, file_path)
    print("Successfully added habit!")
    

def log_habit(habit_name, data):
    if (habit_name not in data):
        print("Error. The task does not exist. Add it first.")
        return

    user_date_input = input("Enter the date you completed the task (YYYY-MM-DD): ")

    try:
        user_date_parsed = datetime.strptime(user_date_input, '%Y-%m-%d')
        user_date_formatted = user_date_parsed.strftime('%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please try again using YYYY-MM-DD.")
        return
    
    data[habit_name][user_date_formatted] = "Completed"
    save_data(data, file_path)
    print("Successfully completed habit!")


def remove_category(habit_name, data):
    if (habit_name not in data):
        print("Habit does not exist")
        return
    if habit_name == "":
        print("Enter valid name")
        return
    data.pop(habit_name)

    save_data(data, file_path)
    print("Successfully removed habit!")


def make_summary(data):
    print("WOULD NOT ADVISE GOING PAST 14 DAYS ON SUMMARY AS VISUALIZATION WILL BE MESSY.")
    summary_choice = str.strip(str.upper((input("Would you like a Day, Week, Month, Year summary (D, W, M, Y)? You can also put a number of days to summarize: "))))

    if summary_choice == 'D':
        return get_last(data, 0) # day
    elif summary_choice == 'W':
        return get_last(data, 7) # week
    elif summary_choice == 'M':
        return get_last(data, 30) # month
    elif summary_choice == 'Y':
        return get_last(data, 365) # year
    elif summary_choice.isnumeric():
        return get_last(data, int(summary_choice))
    else:
        print("Invalid input. Try again with (D, W, M, Y).")
        
        
def get_last(data, days):
    # code for old summary layout without gridding
    # if days <= 1:
    #     date = datetime.today()
    #     date = date.strftime('%Y-%m-%d')
    #     print(f"On {date}, you logged: ")
    #     for habit in data:
    #         if date in data[habit]:
    #             print(f"{habit}")
    # else: 
    #     for i in range(days, -1, -1):
    #         date = datetime.today() - timedelta(days=i)
    #         date = date.strftime('%Y-%m-%d')
    #         print(f"On {date}, you logged: ")
    #         for habit in data:
    #             if date in data[habit]:
    #                 print(f"{habit}")

    date_list = []

    for i in range(days, -1, -1):
        date = datetime.today() - timedelta(days=i)
        date_format = date.strftime('%Y-%m-%d')
        date_list.append(date_format)
    
    headers = ['Habit'] + date_list
    summary_table = []
    for habit in data: # where data is the categories
        row = [habit]
        for date in date_list:
            if date in data[habit]:
                row.append(" ✔ " if data[habit][date] else " X ")
            else:
                row.append(" X ")
        summary_table.append(row)
    print(tabulate(summary_table, headers = headers, tablefmt = "fancy_grid", colalign=("left",) + ("center",) * (len(headers) - 1)))



def create_cli(): 
    while(True):
        print("1. Add new habit category")
        print("2. Log habit")
        print("3. Remove habit category")
        print("4. Show summary")
        print("5. Exit")

        user_choice = input("Option: ")
        data = load_data(file_path)
        if user_choice.isnumeric():
            if user_choice == '1': # add habit
                habit_name = str.strip(str.lower(input("What is the habit name?: "))) 
                add_category(str(habit_name), data)
                input("Press Enter to continue.")
            elif user_choice == '2': # log habit
                habit_name = str.strip(str.lower(input("What is the habit name?: ")))
                log_habit(str(habit_name), data)
                input("Press Enter to continue.")
            elif user_choice == '3': # remove
                habit_name = str.strip(str.lower(input("What is the habit name?: "))) 
                remove_category(str(habit_name), data)
                input("Press Enter to continue.")
            elif user_choice == '4': # summarize
                make_summary(data)
                input("Press Enter to continue.")
            elif user_choice == '5': # exit
                break 
            else:
                "Number is out of range of options."
                input("Press Enter to continue.")
        else:
            print("False Value")
            input("Press Enter to continue.")


if __name__ == "__main__": 
    create_cli()
