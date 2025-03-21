import sys
import os
import tkinter as tk
from tkinter import filedialog


pipe_scripts = os.getenv("PIPE_SCRIPTS_PATH")

def add_scripts_to_path(base_path, subfolder="Editorial_Publisher\davinci_publisher_modular"):
    """Add the scripts path to sys.path if not already included."""
    full_path = os.path.join(base_path, subfolder)

    if not os.path.exists(full_path):
        print(f"Error: path doesnt exist -> {full_path}")
        sys.exit(1)
    
    if full_path not in sys.path:
        sys.path.append(full_path)
        print(f"Added path to sys.path: {full_path}")
    else:
        print(f"Path already in sys.path: {full_path}")

add_scripts_to_path(pipe_scripts)


from project_utils import get_current_project, delete_existing_jobs
from file_utils import export_edl
from render_utils import render_jobs, single_shots_render_settings, full_cut_render_settings




def ask_folders():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    root.lift()  # Bring the window to the front
    root.attributes("-topmost", 1)  # Keep the window on top
    
    output_folder = filedialog.askdirectory(title="Select Render Output Folder")
    export_folder = filedialog.askdirectory(title="Select EDL/OTIO Output Folder") 
    if not output_folder or not export_folder:
        print("Error: Both folders must be selected.")
        sys.exit(1)  # Exit the script if folders are not selected

    return export_folder, output_folder



def main():
    

    export_directory, output_folder = ask_folders()
    print(f"Timeline Export directory: {export_directory}\n Render Output folder: {output_folder} ")

    project = get_current_project(app)
    if not project:
        print("Failed to load current project.")
        sys.exit(1)
    print(f"Succesfully loaded the get current project script: {project.GetName()}")
    try:
        delete_existing_jobs(project)
        export_edl(project, export_directory)
        render_jobs(project)
        print("Rendering completed succesfully")
    except Exception as e:
        print(f"An error occured: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()