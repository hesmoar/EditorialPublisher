# file_utils.py
import os
from timeline_utils import get_timeline_name
import shutil
import json
import pprint
from kitsu_project_context import get_context_from_json
#from render_utils import renders_to_publish, final_full_cut_path

#renders_to_publish = []
test_path = r"D:\HecberryStuff\PAINANI STUDIOS\1_Proyectos\Active\1_Animaorquesta\PipeTest\RenderTest\Clips\moveTest"
new_renders_to_publish = []
json_file_path = r"P:\pipeline\file_tree_test.json"

file_path = r"C:\Temp\KitsuTaskManager\Context\Kitsu_task_context.json"

task_context = get_context_from_json(file_path)

context = {
    "Example_Character": {
        "Project_name": "MyTestProject",
        "Project_short_name": "MTP",
        "Entity_Type": "Assets",
        "AssetType": "character",
        "Entity_Name": "Example_Character_Name",
        "TaskType": "compositing",
        "TaskType_Short_Name": "cmp"
    },
    "Example_Shot": {
        "Project_name": "MyTestProject",
        "Project_short_name": "MTP",
        "Entity_Type": "Shots",
        "Sequence": "Example_Seq01",
        "Entity_Name": "Example_Shot001",
        "TaskType": "compositing",
        "TaskType_Short_Name": "cmp"
    }
}



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

# TODO: In order to add file management functionality, we need to add the context of the shot and task to the window and setup the file tree to work correctly.
# TODO: Renders should be saved in each shot folder inside a specific folder for the task. 
# TODO: Add creation of Output file and Working file in the publishing moment. 

def read_file_tree_json(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            context_data = json.load(file)
            #pprint.pprint(context_data)
        return context_data

    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

#read_file_tree_json(json_file_path)

def map_kitsu_context_to_filetree(context):
    return {
        "Project_short_name": context.get("project_code", ""),
        "Project_name": context.get("project_name", ""),
        "Entity_Type": context.get("entity_type_name", ""),
        "Entity_Name": context.get("entity_name", ""),
        "TaskType": context.get("task_type_name", ""),
        "TaskType_Short_Name": context.get("task_code", ""),
        "Sequence": context.get("sequence", ""),
        "Shot": context.get("entity_name", ""),  # or context.get("shot", "")
        "AssetType": context.get("asset_type", ""),
        "Asset": context.get("asset", ""),
        "Version": "001",      
    }


def replace_placeholders(template, values, style=None):
    for key, value in values.items():
        template = template.replace(f"<{key}>", value)
    
    if style == "lowercase":
        template = template.lower()
    elif style == "uppercase":
        template = template.upper()

    return template
#replace_placeholders()
def generate_paths(json_file_path, context, path_type="working"):
    with open(json_file_path, 'r') as file:
        file_tree = json.load(file)
        #pprint.pprint(file_tree)
    file_tree_section = file_tree.get(path_type)
    print(f"THIS IS FILE TREE SECTION: {file_tree_section}")
    if not file_tree_section:
        raise ValueError(f"Invalid path_type: {path_type}")
    style = file_tree_section["folder_path"].get("style", None)
    folder_paths = {}
    for key, template in file_tree_section["folder_path"].items():
        if key != "style":
            folder_paths[key] = replace_placeholders(template, context, style)
    mountpoint = replace_placeholders(file_tree_section["mountpoint"], context, style)
    full_paths = {key: os.path.join(mountpoint, folder_paths[key]) for key in folder_paths}
    #print("These are the full paths")
    #pprint.pprint(full_paths)
    return full_paths

filetree_context = map_kitsu_context_to_filetree(task_context)
full_paths = generate_paths(json_file_path, filetree_context, path_type="working")

entity_type = filetree_context.get("Entity_Type", "").lower()
print(f"This is the entity type {entity_type}")

if entity_type in full_paths:
    working_dir = full_paths[entity_type]
    print(f"This is the woring directory: {working_dir}")
else:
    working_dir = None
    print(f"Unknown entity type: {entity_type}")

