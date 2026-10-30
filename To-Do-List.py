import json
import os
os.system("")

STRIKE = "\033[9m"
GREY = "\033[90m"
RESET = "\033[0m"

FILE = "stored_tasks.json"

main_options = {
                "1": "Add task", 
                "2": "Check/uncheck task", 
                "3": "Delete task",
                "q": "Quit"
                }

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("Press Enter to continue...")

def sort_tasks(items):
    items.sort(key=lambda task: task["done"])

def save_tasks(tasks):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def load_tasks():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return[]

def menu(title, prompt, options, info=""):
    clear()
    print("=" * 24)
    print(f" {title}")
    print("=" * 24)
    if info:
        print(info)
    print()
    for i in options:
        print(f" {i}) {options[i]}")
    print()
    while True:
        choice = input(prompt)
        if choice in options and options[choice]:
            return choice

def show(description, items, empty_message):
    if items == []:
        print(empty_message)
    else:
        print(description)
        for i in range(0, len(items)):
            if items[i]["done"]:
                print(f" {i+1}) [x] {GREY}{STRIKE}{items[i]['title']}{RESET}")
            else:
                print(f" {i+1}) [ ] {items[i]['title']}")
    print()

def task_text(items):
    if items == []:
        return "No tasks yet"
    lines = []
    for i in range(0, len(items)):
        if items[i]["done"]:
            lines.append(f"{i+1}) [x] {GREY}{STRIKE}{items[i]['title']}{RESET}")
        else:
            lines.append(f"{i+1}) [ ] {items[i]['title']}")
    return ('\n'.join(lines))

def add(prompt, items):
    task = input(prompt)
    if task == "":
        print("The task can not be empty")
        pause()
    else:
        items.append({"title": task, "done": False})
        sort_tasks(items)
        print(f"Added: {task}")
    print()

def mark_done(prompt, tasks):
    show("These are your tasks:", tasks, "There are no active tasks")
    if tasks == []:
        return
        
    answer = input(prompt)
    if not answer.isdigit():
        print("You have to write a number")
        pause()
        return
    
    number = int(answer)
    if number < 1 or number > len(tasks):
        print("There is no task with that number")
        pause()
    else:
        task = tasks[number - 1]
        task["done"] = not task["done"]
        sort_tasks(tasks)
    print()

def delete(prompt, tasks):
    show("These are your tasks:", tasks, "There are no tasks")
    if tasks == []:
        return
    
    answer = input(prompt)
    if answer.lower() == "b":
        print("Cancelled")
        return
    
    if not answer.isdigit():
        print("You have to write a number")
        return

    number = int(answer)
    if number < 1 or number > len(tasks):
        print("There are no tasks with that number")
    
    else:
        removed = tasks.pop(number - 1)
        print(f"Deleted: {removed['title']}")
    
    
    

#---------------------------------------------------------
#--Main
def main():
    tasks = load_tasks()

    while True:
        active = 0
        for task in tasks:
            if not task["done"]:
                active += 1
        choice = menu("Truely Done", "Option: ", main_options,task_text(tasks))
        clear()

        if choice == "1":
            add("Add task: ", tasks)
        elif choice == "2":
            mark_done("Which task do you want to check/uncheck? (number): ", tasks)
        elif choice == "3":
            delete("Which task do you want to delete? (number, enter 'b' to cancel): ", tasks)
        elif choice == "q":
            break

        save_tasks(tasks)
        pause()

main()