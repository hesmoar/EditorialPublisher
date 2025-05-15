import kitsu_auth
import gazu
import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import pprint
from kitsu_auth import kitsu_auto_login

file_path = r"C:\Temp\KitsuTaskManager\Context\Kitsu_task_context.json"

def get_context_from_json(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            context_data = json.load(file)
            pprint.pprint(context_data)
            return context_data
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None
    


def project_context():
    project = get_context_from_json(file_path)
    project_name = project.get("project_name")
    print(f"Project name that comes from the context json: {project_name}")
    kitsu_auto_login()
    project_dict = gazu.project.get_project_by_name(project_name)
    if project_dict:
        project_id = project_dict.get("id")
        print(f"Project ID: {project_id}")
        return project_id, project_name
        #pprint.pprint(project_dict)



def task_context():
    task = get_context_from_json(file_path)
    task_id = task.get("task_id")
    task_name = task.get("task_type_name")
    task_code = task.get("task_code")
    
    return task_id, task_name, task_code
    
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


def get_edit_info(selected_project_name):
    project_edits = gazu.edit.all_edits_for_project(selected_project_name)
    if project_edits:
        print(f"edits loaded succesfully")
        for edit in project_edits:
            #edit_url = gazu.edit.get_edit_url(edit)
            edit_name = edit.get("name")
            print(edit_name)
            return edit_name

        #pprint.pprint(project_edits))
    else:
        print("No edit here")