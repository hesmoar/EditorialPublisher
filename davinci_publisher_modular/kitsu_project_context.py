import kitsu_auth
import gazu
import tkinter as tk
from tkinter import simpledialog, messagebox

def get_project():
    active_projects = gazu.project.all_open_projects()


    return active_projects


def select_project():
    """
    Prompts the user to select a project from a list of available projects.
    Retrieves a list of projects, displays their names, and asks the user to 
    select one by entering the corresponding number. The function handles 
    invalid inputs and ensures a valid selection is made.
    Returns:
        str: The name of the selected project.
    """
    projects_to_pick = get_project()
    project_names = [project.get("name") for project in projects_to_pick]

    def on_select():
        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a project")
            return
        selected_project.set(project_names[selected_index[0]])
        root.quit()

    root = tk.Tk()
    root.title("Select Project")
    root.geometry("300x300")

    selected_project = tk.StringVar()

    label = tk.Label(root, text="Please select an active project from the list: ")
    label.pack(pady=10)

    listbox = tk.Listbox(root, selectmode=tk.SINGLE)
    for project in project_names:
        listbox.insert(tk.END, project)
    listbox.pack(pady=10)

    button = tk.Button(root, text="Select", command=on_select)
    button.pack(pady=10)

    root.mainloop()

    selected_project_name = selected_project.get()
    print(f"You selected the following project {selected_project_name}")
    return selected_project_name

