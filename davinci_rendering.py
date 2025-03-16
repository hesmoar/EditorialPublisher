
import os
import sys
import pprint
from davinci_project_context import get_current_project

#export_directory = #Define your path in here. Example: "C:/Users/username/Desktop/Exported_Timelines"
#TO DO
# Need to determine a name for the render job. 
# Need to see if I can take the path from Kitsu
# Need to connect this with edl exporter so that it runs both, when publishing a cut it exports an edl and 
# updates all the shots in kitsu 


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


render_jobs()

