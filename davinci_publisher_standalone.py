
import os
import sys
import pprint
import tkinter as tk
from tkinter import filedialog


#EXPORT_DIRECTORY = r"D:\HecberryStuff\PAINANI STUDIOS\1_Proyectos\Active\1_Animaorquesta\PipeTest"
#OUTPUT_FOLDER = r"D:\HecberryStuff\PAINANI STUDIOS\1_Proyectos\Active\1_Animaorquesta\PipeTest\RenderTest\Clips"


def ask_folders():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    root.lift()  # Bring the window to the front
    root.attributes("-topmost", 1)  # Keep the window on top
    
    output_folder = filedialog.askdirectory(title="Select Render Output Folder")
    export_folder = filedialog.askdirectory(title="Select edl Output Folder") 
    if not output_folder or not export_folder:
        print("Error: Both folders must be selected.")
        sys.exit(1)  # Exit the script if folders are not selected

    return export_folder, output_folder
EXPORT_DIRECTORY, OUTPUT_FOLDER = ask_folders()
print(EXPORT_DIRECTORY, OUTPUT_FOLDER)

def get_current_project():

    resolve = app.GetResolve()
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()
    if not project:
        print("Error: No current project found.")
        return None
    return project

def delete_existing_jobs():
    project = get_current_project()
    project.DeleteAllRenderJobs() 



def get_timeline(project):
    """Get the current timeline of the project."""
    timeline = project.GetCurrentTimeline()
    if not timeline:
        print("Error: No current timeline found.")
        return None
    return timeline

def get_timeline_name(project):
    timeline = get_timeline(project)
    if timeline:
        return f"{project.GetName()}_{timeline.GetName()}"
    return None

#def get_clips_from_timeline():
#    project = get_current_project()
#    timeline = project.GetCurrentTimeline()
#    timeline_items = timeline.GetItemListInTrack("video", 1)
#
#    for item in timeline_items:
#        clip_name = item.GetName()
#        print(f"Clip name: {clip_name}")


def get_unique_filename(base_name, directory, extension=""):
    """Generate a unique filename with an incremental version number."""
    if not os.path.exists(directory):
        print(f"Error: Export directory '{directory}' does not exist.")
        return None, None
    extension = f".{extension}" if extension else ""
    existing_versions = [ 
        int(filename[len(base_name) + 2 : -len(extension)])
        for filename in os.listdir(directory)
        if filename.startswith(base_name) and filename.endswith(extension)
        and filename[len(base_name) + 2 : -len(extension)].isdigit()
    ]

    version = max(existing_versions, default=0) + 1
    filename = f"{base_name}_v{version:03d}{extension}"
    return os.path.join(directory, filename), filename


def export_edl():
    """Export an EDL file with a unique filename."""
    project = get_current_project()
    if not project:
        print("No current project found")
        return False
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        print("No current timeline found")
        return
    
    edl_name = get_timeline_name(project)
    if not edl_name:
        return
    
    edlFilePath, _ = get_unique_filename(edl_name, EXPORT_DIRECTORY, "edl")
    if not edlFilePath:
        return
    try:
        if timeline.Export(edlFilePath, project.EXPORT_EDL):
            print(f"Timeline exported to {edlFilePath} successfully.")
        else:
            print("Timeline export failed.")
    except Exception as e:
        print(f"Error exporting timeline: {e}")

def single_shots_render_settings():
    """Set render settings for individual shots and create render jobs."""

    project = get_current_project()
    if not project:
        print("No current project found")
        return []
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        print("No current timeline found") 
        return []

    project.SetCurrentRenderMode(1)
    render_preset = next(iter(project.GetRenderPresetList()), "DefaultPreset")

    MarkInOut = timeline.GetMarkInOut()
    MarkIn = MarkInOut.get("video", {}).get("in", 0)
    MarkOut = MarkInOut.get("video", {}).get("out", 0)
    

    render_jobs = []
    for clip in timeline.GetItemListInTrack("video", 1):
        clip_start, clip_end = clip.GetSourceStartFrame(), clip.GetSourceEndFrame()

        #print(f"Clip: {clip_name} starts on {clip_start} and ends on {clip_end}")
        if clip_start >= MarkIn and clip_end <= MarkOut:
            render_name = f"{clip.GetName()}_{timeline.GetName()}"


            project.SetRenderSettings({
                "TargetDir": OUTPUT_FOLDER,
                "CustomName": render_name
            })
            render_job = project.AddRenderJob()
            render_jobs.append(render_job)

    
            #print(f"Parameters set for {clip_name} render job, render preset: {render_preset}")
    print(f"Created {len(render_jobs)} shot render jobs (preset: {render_preset})")

    return render_jobs





def full_cut_render_settings():


    project = get_current_project()
    if not project:
        print("No current project found")
        return None, None
    
    project.SetCurrentRenderMode(1)
    render_preset = next(iter(project.GetRenderPresetList()), "DefaultPreset")

    project_name = project.GetName()
    
    

    timeline_name = get_timeline_name(project)
    if not timeline_name:
        return None, None
    
    project.SetRenderSettings({
        "TargetDir": OUTPUT_FOLDER,
        "CustomName": timeline_name
    })
    full_cut_render_job = project.AddRenderJob()

    print(f"Created full cut render job (preset: {render_preset})")

    return full_cut_render_job, timeline_name
#full_cut_render_settings()

def get_unique_renderJob_name():
    """Ensure render job filenames are unique by checking existing ones and updating if necessary."""
    project = get_current_project()
    if not project:
        print("No current project found")
        return []

    single_shots_render_settings()
    full_cut_render_settings()
    updated_jobs = []
    for job in project.GetRenderJobList():
        job_filename = job.get("OutputFilename", "Unknown")
        #print(f"This is the original job filename: {job_output_filename}")
        job_folder = job.get("TargetDir", "Unknown")
        job_id = job.get("JobId", "Unknown")

        base_name, ext = os.path.splitext(job_filename)
        new_filename = get_unique_filename(base_name, job_folder, ext.lstrip("."))[1]
        #print(f"This is the adjusted filename: {final_render_filename}")
        

        if new_filename != job_filename:
            print(f"Updating job {job_id} filename: {job_filename} to {new_filename}")
            project.DeleteRenderJob(job_id)

            project.SetRenderSettings({
                "TargetDir": job_folder,
                "CustomName": new_filename
            })
            updated_jobs.append(project.AddRenderJob())
        else:

            updated_jobs.append(job_id)
            print(f"Adding job: {job_id}")

    return updated_jobs
    

def render_jobs():
    """Render all jobs after ensuring unique filenames."""
    project = get_current_project()
    if not project:
        return
    #single_shot_render_job = single_shots_render_settings()
    #full_cut_render_job = full_cut_render_settings()
    jobs_to_render = get_unique_renderJob_name()
    print(f"Rendering jobs {jobs_to_render}")
    #print(f"Render jobs {single_shot_render_job} and {full_cut_render_job} created successfully.")
    if jobs_to_render:
        project.StartRendering(jobs_to_render)





if __name__ == "__main__":
    delete_existing_jobs()
    export_edl()
    render_jobs()

