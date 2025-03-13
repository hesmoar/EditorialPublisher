
import os
import sys
import pprint


export_directory = r"D:\HecberryStuff\PAINANI STUDIOS\1_Proyectos\Active\1_Animaorquesta\PipeTest"
output_folder = r"D:\HecberryStuff\PAINANI STUDIOS\1_Proyectos\Active\1_Animaorquesta\PipeTest\RenderTest\Clips"

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
        return None, None
    version = 1
    while True:
        if extension:
            filename = f"{base_name}_v{version:03d}.{extension}"
        else:
            filename = f"{base_name}_v{version:03d}"
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            return filepath, filename
        version += 1


def export_edl():
    edl_name = get_timeline_name()
    if not edl_name:
        return
    edlFilePath, edlFilename = get_unique_filename(edl_name, export_directory, "edl")
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
    #print(MarkIn)
    render_jobs = []


    for clip in timeline_items:
        clip_name = clip.GetName()
        clip_start = clip.GetSourceStartFrame()
        clip_end = clip.GetSourceEndFrame()
        #print(f"Clip: {clip_name} starts on {clip_start} and ends on {clip_end}")
        if clip_start >= MarkIn and clip_end <= MarkOut:
            render_name = clip_name + "_" + timeline_name


            render_settings = project.SetRenderSettings({
                "TargetDir": output_folder,
                "CustomName": render_name
            })
            render_job = project.AddRenderJob()
            render_jobs.append(render_job)

    
            print(f"Parameters set for {clip_name} render job, render preset: {render_preset}")

    #print(render_jobs)
    return render_jobs
#single_shots_render_settings()




def full_cut_render_settings():

    project = get_current_project()
    project_renderMode = project.SetCurrentRenderMode(1)
    render_preset_list = project.GetRenderPresetList()
    render_preset = project.GetRenderPresetList()[0]  # Use first preset
    project_name = project.GetName()
    
    

    timeline_name = project.GetCurrentTimeline().GetName()
    full_cut_filename = project_name + "_" + timeline_name

    
    render_settings = project.SetRenderSettings({
        "TargetDir": output_folder,
        "CustomName": full_cut_filename
    })
    full_cut_render_job = project.AddRenderJob()

    print(f"Parameters set for: {project_name} full cut, render preset: {render_preset}")

    return full_cut_render_job, full_cut_filename
#full_cut_render_settings()

def get_unique_renderJob_name():
    project = get_current_project()
    single_shots_render_job = single_shots_render_settings()
    full_cut_render_job = full_cut_render_settings()
    project_render_jobs = project.GetRenderJobList()#single_shots_render_job)
    pprint.pprint(project_render_jobs)
    #print(project_render_jobs[2].get("OutputFilename"))
    #pprint.pprint(job_info)
    jobs_to_render = []
    for job in project_render_jobs:
        job_output_filename = job.get("OutputFilename", "Unknown")
        print(f"This is the original job filename: {job_output_filename}")
        job_output_folder = job.get("TargetDir", "Unknown")
        job_id = job.get("JobId", "Unknown")
        base_name, extension = os.path.splitext(job_output_filename)
        extension = extension.lstrip(".")
        final_render_filename = get_unique_filename(base_name, job_output_folder, extension)[1]
        print(f"This is the adjusted filename: {final_render_filename}")
        #pprint.pprint(job)

        if final_render_filename != job_output_filename:
            print(f"Final render job name: {final_render_filename} is different")
            project.DeleteRenderJob(job_id)

            project.SetRenderSettings({
                "TargetDir": job_output_folder,
                "CustomName": final_render_filename
            })
            new_render_job = project.AddRenderJob()
            jobs_to_render.append(new_render_job)
        else:
            #job["OutputFilename"] = final_render_filename
        #print(f"Final render job name: {final_render_filename}")
            jobs_to_render.append(job_id)
        pprint.pprint(f"These are the final names: {job.get("OutputFilename")}")

    return jobs_to_render
    


#get_unique_renderJob_name()


def render_jobs():
    project = get_current_project()
    #single_shot_render_job = single_shots_render_settings()
    #full_cut_render_job = full_cut_render_settings()
    jobs_to_render = get_unique_renderJob_name()
    print(jobs_to_render)
    #print(f"Render jobs {single_shot_render_job} and {full_cut_render_job} created successfully.")
    project.StartRendering(jobs_to_render)
render_jobs()




if __name__ == "__main__":
    export_edl()
    render_jobs()

