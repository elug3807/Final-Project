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
                "4": "Search tasks",
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
        return
    
    number = int(answer)
    if number < 1 or number > len(tasks):
        print("There is no task with that number")
    else:
        task = tasks[number - 1]
        task["done"] = not task["done"]
        sort_tasks(tasks)
    print()

def search(prompt, tasks):
    text = input(prompt).strip().lower()
    if text == "":
        print("The search can not be empty")
        return

    print()
    found = 0
    for i in range(0, len(tasks)):
        if text in tasks[i]["title"].lower():
            if tasks[i]["done"]:
                print(f" {i+1}) [x] {GREY}{STRIKE}{tasks[i]['title']}{RESET}")
            else:
                print(f" {i+1}) [ ] {tasks[i]['title']}")
            found += 1

    if found == 0:
        print("No tasks contain that text")

def delete_one(tasks):
    show("These are your tasks:", tasks, "There are no tasks")
    if tasks == []:
        return

    answer = input("Which task do you want to delete? (number")

    if not answer.isdigit():
        print("You have to write a number")
        return

    number = int(answer)
    if number < 1 or number > len(tasks):
        print("There is no task with that number")
    else:
        removed = tasks.pop(number - 1)
        print(f"Deleted: {removed['title']}")
    

def delete_completed(tasks):
    kept = []
    for task in tasks:
        if not task["done"]:
            kept.append(task)

    removed = len(tasks) - len(kept)
    if removed  == 0:
        print("There are no completed tasks")
        return

    answer = input(f"Delete {removed} completed tasks? (y/n): ")
    if answer.lower()=="y":
        tasks[:] = kept
        print(f"Deleted {removed} completed tasks")
    else:
        print("Cancelled")

delete_options = {
                    "1": "Delete one task",
                    "2": "Delete all completed tasks",
                    "b": "Back"
                 }

def delete_menu(tasks):
    while True:
        choice = menu("Delete tasks", "Option: ", delete_options, task_text(tasks))
        clear()

        if choice == "1":
            delete_one(tasks)
        elif choice == "2":
            delete_completed(tasks)
        elif choice == "b": 
            return
        save_tasks(tasks)
        pause()

#---------------------------------------------------------
#--Main
def main():
    tasks = load_tasks()

    while True:
        choice = menu("Truely Done", "Option: ", main_options,task_text(tasks))
        clear()

        if choice == "1":
            add("Add task: ", tasks)
        elif choice == "2":
            mark_done("Which task do you want to check/uncheck?", tasks)
        elif choice == "3":
            delete_menu(tasks)
            continue
        elif choice == "4":
            search("Search for: ", tasks)
        elif choice == "q":
            break

        save_tasks(tasks)
        pause()

main()