import os

main_options = {"1": "Show tasks", "2": "Add task", "3": "Mark task as done", "4": "Show completed tasks", "q": "Quit"}

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("Press Enter to continue...")

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
            print(f" {i+1}) {items[i]}")
    print()

def add(prompt, items):
    task = input(prompt)
    if task == "":
        print("The task can not be empty")
    else:
        items.append(task)
        print(f"Added: {task}")
    print()

def mark_done(prompt, tasks, done):
    show("These are your tasks:", tasks, "There are no active tasks")
    if tasks == []:
        return
    answer = input(prompt)
    if not answer.isdigit():
        print("You have to write a number")
        print()
        return
    number = int(answer)
    if number < 1 or number > len(tasks):
        print("There is no task with that number")
    else:
        task = tasks.pop(number - 1)
        done.append(task)
        print(f"{task} is done!")
    print()

#---------------------------------------------------------
#--Main
def main():
    lists = {"tasks": [], "done": []}

    while True:
        info = f" {len(lists['tasks'])} active, {len(lists['done'])} completed"
        choice = menu("Truely Done", "Option: ", main_options, info)
        clear()

        if choice == "1":
            show("These are your tasks:", lists["tasks"], "There are no active tasks")
        elif choice == "2":
            add("Add task: ", lists["tasks"])
        elif choice == "3":
            mark_done("Which task is done? (number): ", lists["tasks"], lists["done"])
        elif choice == "4":
            show("These tasks are done:", lists["done"], "There are no completed tasks")
        elif choice == "q":
            break

        pause()

main()