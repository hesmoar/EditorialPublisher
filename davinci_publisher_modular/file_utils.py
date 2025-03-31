# file_utils.py
import os
from timeline_utils import get_timeline_name

#renders_to_publish = []


def get_unique_filename(base_name, directory, extension=""):
    """Generate a unique filename with an incremental version number."""
    if not os.path.exists(directory):
        print(f"Error: Export directory '{directory}' does not exist.")
        return None, None
    extension = f".{extension}" if extension else ""
    existing_versions = [ 
        int(filename[len(base_name) + 2 : -len(extension)] )
        for filename in os.listdir(directory)
        if filename.startswith(base_name) and filename.endswith(extension)
        and filename[len(base_name) + 2 : -len(extension)].isdigit()
    ]

    version = max(existing_versions, default=0) + 1
    filename = f"{base_name}_v{version:03d}{extension}"
    full_file_path = os.path.join(directory, filename)
    #renders_to_publish.append(full_file_path)
    #print(f"These are all the renders we need to publish: {renders_to_publish}")
    return os.path.join(directory, filename), filename

def export_edl(project, export_directory):
    """Export an EDL file with a unique filename."""
    timeline = project.GetCurrentTimeline()
    if not timeline:
        print("No current timeline found.")
        return False
    
    edl_name = get_timeline_name(project)
    if not edl_name:
        return None
    
    edlFilePath, _ = get_unique_filename(edl_name, export_directory, "edl")
    if not edlFilePath:
        return
    
    try:
        if timeline.Export(edlFilePath, project.EXPORT_EDL):
            print(f"Timeline exported to {edlFilePath} successfully.")
        else:
            print("Timeline export failed.")
    except Exception as e:
        print(f"Error exporting timeline: {e}")
    return edlFilePath


def export_otio(project, export_directory):
    """Export an OTIO file with a unique filename"""
    timeline = project.GetCurrentTimeline()
    if not timeline:
        print("No current timeline found.")
        return False
    
    otio_name = get_timeline_name(project)
    if not otio_name:
        return None
    
    otioFilePath, _ = get_unique_filename(otio_name, export_directory, "otio")
    if not otioFilePath:
        return
    
    try:
        if timeline.Export(otioFilePath, project.EXPORT_OTIO):
            print(f"SUCCESFULLY EXPORTED TIMELINE TO: {otioFilePath}")
        else:
            print("Timeline export failed.")
    except Exception as e:
        print(f"Error exporting timeline: {e}")
    return otioFilePath
