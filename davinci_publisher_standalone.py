
import os
import sys
import pprint


export_directory = r"D:\HecberryStuff\PAINANI STUDIOS\1_Proyectos\Active\1_Animaorquesta\PipeTest"
output_folder = r"D:\HecberryStuff\PAINANI STUDIOS\1_Proyectos\Active\1_Animaorquesta\PipeTest\RenderTest"

def get_current_project():

    resolve = app.GetResolve()
    projectManager = resolve.GetProjectManager()
    current_project = projectManager.GetCurrentProject()
    if not current_project:
        print("Error: No current project found.")
        return None
    project = current_project.GetName()
    return current_project

def get_timeline_name():
    project = get_current_project()
    if not project:
        return None
    timeline = project.GetCurrentTimeline()
    if not timeline:
        print("Error: No current timeline found.")
    timeline_name = timeline.GetName()
    project_name = project.GetName()
    edl_name = project_name + "_" + timeline_name
    return edl_name

def get_clips_from_timeline():
    project = get_current_project()
    timeline = project.GetCurrentTimeline()
    timeline_items = timeline.GetItemListInTrack("video", 1)

    for item in timeline_items:
        clip_name = item.GetName()
        print(f"Clip name: {clip_name}")


def get_unique_filename(base_name, directory, extension=None):
    if not os.path.exists(directory):
        print(f"Error: Export directory '{directory}' does not exist.")
        return None
    version = 1
    while True:
        if extension:
            filename = f"{base_name}_v{version:03d}.{extension}"
        else:
            filename = f"{base_name}_v{version:03d}"
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            return filepath
        version += 1


def export_edl():
    edl_name = get_timeline_name()
    if not edl_name:
        return
    edlFilePath = get_unique_filename(edl_name, export_directory, "edl")
    if not edlFilePath:
        return
    if not os.path.isdir(os.path.dirname(edlFilePath)):
        print(f"Error: The directory part of the file path '{edlFilePath}' is not a valid directory.")
        return
    project = get_current_project()
    timeline = project.GetCurrentTimeline()
    try:
        result = timeline.Export(edlFilePath, project.EXPORT_EDL)
        if result:
            print(f"Timeline exported to {edlFilePath} successfully.")
        else:
            print("Timeline export failed. Unknown reason.")
    except Exception as e:
        print(f"Timeline export failed. Error: {e}")


def single_shots_render_settings(): 

    project = get_current_project()
    timeline = project.GetCurrentTimeline()


    project_name = project.GetName()
    timeline_name = project.GetCurrentTimeline().GetName()

    project_renderMode = project.SetCurrentRenderMode(1)
    render_preset = project.GetRenderPresetList()[0]  # Use first preset
    
    
    timeline_items = timeline.GetItemListInTrack("video", 1)
    MarkInOut = timeline.GetMarkInOut()
    MarkIn = MarkInOut.get("video", {}).get("in", 0)
    MarkOut = MarkInOut.get("video", {}).get("out", 0)
    print(MarkIn)
  


    for clip in timeline_items:
        clip_name = clip.GetName()
        clip_start = clip.GetSourceStartFrame()
        clip_end = clip.GetSourceEndFrame()
        #print(f"Clip: {clip_name} starts on {clip_start} and ends on {clip_end}")
        if clip_start >= MarkIn and clip_end <= MarkOut:
            render_name = clip_name + "_" + timeline_name
            filename = get_unique_filename(render_name, output_folder)


            render_settings = project.SetRenderSettings({
                "TargetDir": output_folder,
                "CustomName": render_name
            })

            single_shots_render_job = project.AddRenderJob()
    
            print(f"Parameters set for {clip_name} render job, render preset: {render_preset}")


    return single_shots_render_job
#single_shots_render_settings()




def full_cut_render_settings():

    project = get_current_project()
    project_renderMode = project.SetCurrentRenderMode(1)
    render_preset_list = project.GetRenderPresetList()
    render_preset = project.GetRenderPresetList()[0]  # Use first preset
    project_name = project.GetName()
    
    

    timeline_name = project.GetCurrentTimeline().GetName()
    Filename = project_name + "_" + timeline_name + "_render"
    full_cut_name = get_unique_filename(Filename, output_folder)
    
    render_folder = project.SetRenderSettings({
        "TargetDir": output_folder,
        "CustomName": Filename
    })
    full_cut_render_job = project.AddRenderJob()
    #full_cut_render = project.GetRenderJobList(full_cut_render_job)
    #pprint.pprint(full_cut_render)
    print(f"Parameters set for render job for project: {project_name}, render preset: {render_preset}")

    return full_cut_render_job

def get_unique_renderJob_name():
    project = get_current_project()
    full_cut_render_job = full_cut_render_settings()
    job_info = project.GetRenderJobList(full_cut_render_job)
    #pprint.pprint(job_info)
    job_path = job_info[1].get("TargetDir")
    job_name = job_info[1].get("OutputFilename")

    file_exists = get_unique_filename(job_name, job_path)
    print(file_exists)
    #print(job_path +  job_name)

get_unique_renderJob_name()


def render_jobs():
    project = get_current_project()
    single_shot_render_job = single_shots_render_settings()
    full_cut_render_job = full_cut_render_settings()
    print(f"Render jobs {single_shot_render_job} and {full_cut_render_job} created successfully.")
    #project.StartRendering(single_shots_render_settings, full_cut_render_settings)




if __name__ == "__main__":
    export_edl()
    render_jobs()

