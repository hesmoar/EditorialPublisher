import sys
import os


pipe_scripts = os.getenv("PIPE_SCRIPTS_PATH")

def add_scripts_to_path(base_path, subfolder=r"Editorial_Publisher\davinci_publisher_modular"):
    """Add the scripts path to sys.path if not already included."""
    full_path = os.path.join(base_path, subfolder)

    if not os.path.exists(full_path):
        print(f"Error: path doesnt exist -> {full_path}")
        sys.exit(1)
    
    if full_path not in sys.path:
        sys.path.append(full_path)
        print(f"Succesfully loaded PIPE_SCRIPTS_PATH ")#Added path to sys.path": {full_path}")
    else:
        print(f"Path already in sys.path: {full_path}")

add_scripts_to_path(pipe_scripts)

# Import your existing modules
from gui import run_gui
from project_utils import get_current_project, delete_existing_jobs
from file_utils import export_edl, export_otio
from render_utils import render_jobs, single_shots_render_settings, full_cut_render_settings
from kitsu_auth import connect_to_kitsu
from kitsu_editorial_publisher import read_edl, read_otio, update_kitsu


def main():
    """Main function to run the script with GUI selections"""
    
    # Run the GUI and get the selections
    selections = run_gui()

    # Extract the selections
    export_folder = selections.get("export_folder")
    output_folder = selections.get("output_folder")
    should_export_otio = selections.get("export_otio")
    render_single_shots = selections.get("render_single_shots")
    render_full_cut = selections.get("render_full_cut")
    should_update_kitsu = selections.get("update_kitsu")

    print("\nSelected Options:")
    print(f"Export Folder: {export_folder}")
    print(f"Output Folder: {output_folder}")
    print(f"Export OTIO: {should_export_otio}")
    print(f"Render Single Shots: {render_single_shots}")
    print(f"Render Full Cut: {render_full_cut}")
    print(f"Update Kitsu: {should_update_kitsu}")

    # Get current project
    project = get_current_project(app)
    if not project:
        print("Failed to load current project.")
        sys.exit(1)
    print(f"Succesfully loaded the get current Resolve project: {project.GetName()}")

    try:
        # Delete existing jobs
        delete_existing_jobs(project)

        # Export OTIO if selected
        if should_export_otio:
            export_otio(project, export_folder)
            
        # Render single shots, full cut, or both
        render_jobs(
            project,
            output_folder,
            render_single_shots=selections.get("render_single_shots", True),
            render_full_cut=selections.get("render_full_cut", True)
        )
        #if render_single_shots:
            #single_shots_render_settings(project, output_folder)

        #if render_full_cut:
            #full_cut_render_settings(project, output_folder)

        # Update on Kitsu if selected
        if should_update_kitsu:
            connect_to_kitsu()
            otio_file_path = export_otio(project, export_folder)
            read_otio(otio_file_path)
            update_kitsu(otio_file_path)

        print("Process completed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
