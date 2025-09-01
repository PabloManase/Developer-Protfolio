"""
Task Manager Application
------------------------

This program provides a simple task management system with user login,
task assignment, and reporting functionality.

Features:
- User authentication (loaded from user.txt).
- Admin-only user registration.
- Add new tasks with validation.
- View all tasks or only those assigned to the logged-in user.
- Edit or mark personal tasks as complete.
- Generate detailed reports (task_overview.txt and user_overview.txt).
- Display statistics (admin only).

Data Files:
- user.txt : Stores usernames and passwords in 'username, password' format.
- tasks.txt : Stores tasks in 'username, title, description, due_date,
  assigned_date, completed' format.

Admin User:
- A default 'admin, admin' account is created automatically
  if user.txt does not exist.

Author: Paballo
"""


# ===== Importing external modules ============
from datetime import datetime
import os


# ---- Helper Functions ----

def reg_user():
    """
    Register a new user (admin only).

    Prompts the admin to enter a new username and password.
    Validates duplicate usernames and ensures password confirmation matches.
    Saves the new user to user.txt.
    """
    if username != "admin":
        print("Only admin can register new users.")
        return

    new_user = input("Enter new username: ")
    if new_user in username_password:
        print("Username already exists.")
        return

    new_password = input("Enter new password: ")
    confirm_password = input("Confirm password: ")
    if new_password == confirm_password:
        username_password[new_user] = new_password
        with open("user.txt", "a") as user_file:
            user_file.write(f"\n{new_user}, {new_password}")
        print("New user registered successfully.")
    else:
        print("Passwords do not match.")


def add_task():
    """
    Allow a user to add a new task.

    Prompts for:
    - Assigned user (must exist).
    - Task title and description.
    - Due date in YYYY-MM-DD format.
    Automatically assigns today's date as assigned_date
    and defaults 'completed' to 'No'.
    Appends the new task to tasks.txt.
    """
    assigned_user = input(
        "Enter username of the person the task is assigned to: "
    )
    if assigned_user not in username_password:
        print("User does not exist.")
        return

    task_title = input("Enter task title: ")
    task_description = input("Enter task description: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    assigned_date = datetime.today().strftime("%Y-%m-%d")

    task_entry = (
        f"{assigned_user}, {task_title}, {task_description}, "
        f"{due_date}, {assigned_date}, No\n"
    )

    with open("tasks.txt", "a") as task_file:
        task_file.write(task_entry)
    print("Task added successfully.")


def view_all():
    """Display all tasks in the system."""
    try:
        with open("tasks.txt", "r") as task_file:
            tasks = []
            for line in task_file:
                if line.strip():
                    tasks.append(line.strip().split(", "))

    except FileNotFoundError:
        print("No tasks found.")
        return

    if not tasks:
        print("No tasks to display.")
        return

    for i, task in enumerate(tasks, 1):
        print(
            f"""
            Task {i}
            User: {task[0]}
            Title: {task[1]}
            Description: {task[2]}
            Due date: {task[3]}
            Assigned date: {task[4]}
            Completed: {task[5]}
            """
        )


def view_mine():
    """
    Display tasks assigned to the current user.

    Allows user to:
    - Mark a task as complete.
    - Edit the assigned user or due date (if not yet completed).
    Validates usernames and due date format.
    Updates the correct task entry in tasks.txt.
    """
    try:
        with open("tasks.txt", "r") as task_file:
            tasks = []
            for line in task_file:
                if line.strip():
                    tasks.append(line.strip().split(", "))

    except FileNotFoundError:
        print("No tasks file found. Please add a task first.")
        return

    # Get tasks belonging to this user
    user_task_indices = [i for i, t in enumerate(tasks) if t[0] == username]

    if not user_task_indices:
        print("No tasks assigned to you.")
        return

    # Display tasks
    for idx, task_index in enumerate(user_task_indices, start=1):
        task = tasks[task_index]
        print(
            f"""
            Task {idx}
            Title: {task[1]}
            Description: {task[2]}
            Due date: {task[3]}
            Assigned date: {task[4]}
            Completed: {task[5]}
            """
        )

    try:
        choice = int(
            input(
                    "Enter task number to edit/mark complete (-1 to return): "
                )
            )
    except ValueError:
        print("Invalid input.")
        return

    if choice == -1:
        return

    if choice < 1 or choice > len(user_task_indices):
        print("Invalid task number.")
        return

    # Map back to original index in tasks list
    real_index = user_task_indices[choice - 1]
    selected_task = tasks[real_index]

    # Action selection
    action = input("Mark as complete (c) or edit (e): ").lower()
    if action == "c":
        selected_task[5] = "Yes"
    elif action == "e":
        if selected_task[5] == "Yes":
            print("Task cannot be edited (already complete).")
            return

        # Validate new username
        new_user = input("Enter new username: ")
        if new_user not in username_password:
            print("Invalid username. Task not reassigned.")
            return

        # Validate new due date
        new_due = input("Enter new due date (YYYY-MM-DD): ")
        try:
            datetime.strptime(new_due, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Task not updated.")
            return

        # Apply changes
        selected_task[0] = new_user
        selected_task[3] = new_due
    else:
        print("Invalid action.")
        return

    # Save back to file
    with open("tasks.txt", "w") as task_file:
        task_file.writelines([", ".join(t) + "\n" for t in tasks])

    print("Task updated successfully.")


def generate_reports():
    """
    Generate reports summarizing tasks and users.

    Creates:
    - task_overview.txt: Overall stats on tasks (totals, percentages).
    - user_overview.txt: Per-user stats(counts/percentages of task status).
    """
    try:
        with open("tasks.txt", "r") as task_file:
            tasks = []
            for line in task_file:
                if line.strip():
                    tasks.append(line.strip().split(", "))

    except FileNotFoundError:
        print("No tasks file found. Cannot generate reports.")
        return

    total_tasks = len(tasks)
    completed = sum(1 for t in tasks if t[5] == "Yes")
    incomplete = total_tasks - completed
    overdue = sum(
        1 for t in tasks
        if (
            t[5] == "No"
            and datetime.strptime(t[3], "%Y-%m-%d") < datetime.today()
        )
    )

    # ---- Task Overview ----
    with open("task_overview.txt", "w") as f:
        f.write("=== Task Overview ===\n")
        f.write(f"Total tasks: {total_tasks}\n")
        f.write(f"Completed: {completed}\n")
        f.write(f"Incomplete: {incomplete}\n")
        f.write(f"Overdue: {overdue}\n")

        if total_tasks > 0:
            f.write(f"% Incomplete: {incomplete / total_tasks * 100:.2f}%\n")
            f.write(f"% Overdue: {overdue / total_tasks * 100:.2f}%\n")

    # ---- User Overview ----
    with open("user_overview.txt", "w") as f:
        f.write("=== User Overview ===\n")
        f.write(f"Total users: {len(username_password)}\n")
        f.write(f"Total tasks: {total_tasks}\n")

        for user in username_password:
            user_tasks = [t for t in tasks if t[0] == user]
            total_user = len(user_tasks)
            completed_user = sum(1 for t in user_tasks if t[5] == "Yes")
            incomplete_user = total_user - completed_user
            overdue_user = sum(
                1 for t in user_tasks
                if (
                    t[5] == "No"
                    and datetime.strptime(t[3], "%Y-%m-%d") < datetime.today()
                )
            )

            f.write(f"\n--- {user} ---\n")
            f.write(f"Total tasks: {total_user}\n")

            if total_tasks > 0:
                f.write(
                    f"% of all tasks: {total_user / total_tasks * 100:.2f}%\n"
                )

            if total_user > 0:
                f.write(f"Completed: {completed_user}\n")
                f.write(f"Incomplete: {incomplete_user}\n")
                f.write(f"Overdue: {overdue_user}\n")
                f.write(
                    f"% Completed: {completed_user / total_user * 100:.2f}%\n"
                )
                f.write(
                    f"% Incomplete: {incomplete_user/total_user * 100:.2f}%\n"
                )
                f.write(f"% Overdue: {overdue_user / total_user * 100:.2f}%\n")


def display_statistics():
    """
    Display system statistics (admin only).

    Automatically generates reports and prints
    the contents of task_overview.txt and user_overview.txt to the console.
    """
    if username != "admin":
        print("Only admin can view statistics.")
        return

    generate_reports()

    with open("task_overview.txt", "r") as f:
        print(f.read())
    with open("user_overview.txt", "r") as f:
        print(f.read())


# ---- Main Program ----

# Ensure required file exist
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as f:
        # Create default admin account if file doesn't exist
        f.write("admin, admin\n")

# Ensure required file exist
if not os.path.exists("tasks.txt"):
    # Create an empty file to avoid FileNotFoundError
    open("tasks.txt", "w").close()

# Load users
username_password = {}
with open("user.txt", "r") as user_file:
    for line in user_file:
        if line.strip():
            try:
                user, pw = line.strip().split(", ")
                username_password[user] = pw
            except ValueError:
                # Skip malformed lines instead of crashing
                continue


# Login
while True:
    username = input("Username: ")
    password = input("Password: ")
    if (
        username in username_password
        and username_password[username] == password
    ):

        print("Login successful.")
        break
    else:
        print("Invalid credentials.")

# Menu loop
while True:
    if username == "admin":
        menu = input(
            """
            Select one of the following options:
            r  - Register a user
            a  - Add a task
            va - View all tasks
            vm - View my tasks
            gr - Generate reports
            ds - Display statistics
            e  - Exit
            :
            """
        ).lower()
    else:
        menu = input(
            """
            Select one of the following options:
            a  - Add a task
            va - View all tasks
            vm - View my tasks
            e  - Exit
            :
            """
        ).lower()

    if menu == "r" and username == "admin":
        reg_user()
    elif menu == "a":
        add_task()
    elif menu == "va":
        view_all()
    elif menu == "vm":
        view_mine()
    elif menu == "gr" and username == "admin":
        generate_reports()
    elif menu == "ds" and username == "admin":
        display_statistics()
    elif menu == "e":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Try again.")
