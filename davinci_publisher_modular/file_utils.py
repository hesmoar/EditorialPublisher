# file_utils.py
import os
from timeline_utils import get_timeline_name
import shutil
#from render_utils import renders_to_publish, final_full_cut_path

#renders_to_publish = []
test_path = r"D:\HecberryStuff\PAINANI STUDIOS\1_Proyectos\Active\1_Animaorquesta\PipeTest\RenderTest\Clips\moveTest"
new_renders_to_publish = []

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

# In here we have to add file management functionality, so that it moves the files to the correct folder. 

def move_files_to_publish_directory(single_shot_render_path):#, full_cut_render_path):
    """First we need to move the files and then we need to publish them from that new location so that info is updated in Kitsu"""
    for file in single_shot_render_path:
        if os.path.exists(file):
            #new_file_path = os.path.join(full_cut_render_path, os.path.basename(file))
            new_file_path = os.path.join(test_path, os.path.basename(file))
            try:
                shutil.move(file, new_file_path)
                print(f"Moved {file} to {new_file_path}")
                new_renders_to_publish.append(new_file_path)
                #single_shot_render_path.remove(file)
                #single_shot_render_path.append(new_file_path)
            except Exception as e:
                print(f"Error moving file {file}: {e}")
        else:
            print(f"File {file} does not exist.")
    print(f"This is the new list of file paths: {single_shot_render_path}")