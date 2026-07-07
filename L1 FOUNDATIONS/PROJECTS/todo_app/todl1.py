from todo_manage import Task_Manager

manager = Task_Manager()

while True:
    print("\n===== TODO APP =====")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        title = input("Enter task: ")
        manager.add_task(title)

    elif choice == "2":
        manager.view_tasks()

    elif choice == "3":
        manager.view_tasks()
        task = input("Enter task number to complete: ")
        manager.complete_task(task)

    elif choice == "4":
        manager.view_tasks()
        task = input("Enter task number to delete: ")
        manager.delete_task(task)

    elif choice == "5":
        print("Goodbye")
        break

    else:
        print("Invalid choice. Please try again.")