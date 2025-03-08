import os
import sys

export_directory = r"D:\HecberryStuff\PAINANI STUDIOS\1_Proyectos\Active\1_Animaorquesta\PipeTest"

resolve = app.GetResolve()
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
timeline = project.GetCurrentTimeline()
timeline_name = timeline.GetName()
edl_name = timeline_name + "_v001.edl"




def get_unique_filename(base_name, directory, extension):
    version = 1
    while True:
        filename = f"{base_name}_v{version:03d}.{extension}"
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            return filepath
        version += 1

edlFilePath = get_unique_filename(timeline_name, export_directory, "edl")
#print(edlFilePath)

def Export(timeline, filePath, exportType, exportSubType=None):
    try:
        result = None
        if exportSubType is None:
            result = timeline.Export(filePath, exportType)
        else:
            result = timeline.Export(filePath, exportType, exportSubType)

        if result:
            print("Timeline exported to {0} successfully.".format(filePath))
        else:
            print(f"Timeline export failed. Unknown reason.")
    except Exception as e:
        print(f"Timeline export failed. Error: {e}")



#Check if the timeline object exists.
if not timeline:
    print("Error: No current timeline found.")

#Check if the export directory is valid.
if not os.path.exists(export_directory):
    print(f"Error: Export directory '{export_directory}' does not exist.")

#Check if the file path is valid.
if not os.path.isdir(os.path.dirname(edlFilePath)):
    print(f"Error: The directory part of the file path '{edlFilePath}' is not a valid directory.")




Export(timeline, edlFilePath, resolve.EXPORT_EDL)