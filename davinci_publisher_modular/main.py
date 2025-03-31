import sys
import os


pipe_scripts = os.getenv("PIPE_SCRIPTS_PATH")
render_presets = []

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
from file_utils import export_otio
from render_utils import render_jobs, get_render_presets, get_render_status
from kitsu_auth import connect_to_kitsu
from kitsu_editorial_publisher import read_edl, read_otio, update_kitsu, files_to_publish


def main():
    """Main function to run the script with GUI selections"""
    # Get current project
    project = get_current_project(app)
    if not project:
        print("Failed to load current project.")
        sys.exit(1)
    print(f"Succesfully loaded the get current Resolve project: {project.GetName()}")

    # Get render presets to populate GUI
    try:
        render_presets_dict = get_render_presets(project)
        if render_presets_dict:
            print("Succesfully loaded project render presets")
        for key, value in render_presets_dict.items():
            render_presets.append(value)
    except Exception as e:
        print(f"Failed to load render presets: {e}")
        sys.exit(1)


    # Run the GUI and get the selections
    selections = run_gui(render_presets)

    # Extract the selections
    export_folder = selections.get("export_folder")
    output_folder = selections.get("output_folder")
    should_export_otio = selections.get("export_otio")
    render_single_shots = selections.get("render_single_shots")
    render_section_cut = selections.get("section_render_cut")
    render_full_cut = selections.get("render_full_cut")
    selected_render_preset = selections.get("selected_render_preset")
    should_update_kitsu = selections.get("update_kitsu")

    print("\nSelected Options:")
    print(f"Export Folder: {export_folder}")
    print(f"Output Folder: {output_folder}")
    print(f"Export OTIO: {should_export_otio}")
    print(f"Render Single Shots: {render_single_shots}")
    print(f"Section render cut: {render_section_cut}")
    print(f"Render Full Cut: {render_full_cut}")
    print(f"Selected Render preset: {selected_render_preset}")
    print(f"Update Kitsu: {should_update_kitsu}")


    try:
        # Delete existing jobs
        delete_existing_jobs(project)
        get_render_presets(project)
        # Export OTIO if selected
        if should_export_otio:
            export_otio(project, export_folder)
            
        # Render single shots, full cut, or both
        render_jobs(
            project,
            selected_render_preset,
            output_folder,
            render_single_shots=selections.get("render_single_shots", True),
            render_section_cut=selections.get("render_section_cut", True),
            render_full_cut=selections.get("render_full_cut", True)
        )

        # Update on Kitsu if selected
        if should_update_kitsu:
            get_render_status(project)
            connect_to_kitsu()
            otio_file_path = export_otio(project, export_folder)
            read_otio(otio_file_path)
            update_kitsu(otio_file_path)
            files_to_publish()

        print("Process completed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
