import os
import pprint
from timeline_utils import get_timeline, get_clips_from_timeline, get_timeline_name, get_timeline_markers, get_timeline_markInOut
from file_utils import get_unique_filename
from project_utils import get_current_project


full_cut_ranges = {}
section_cut_ranges = {}
shot_cut_ranges = {}




def get_timeline_marks(project):
    """Get and store the full cut frame range from the timeline."""

    full_cut_markIn, full_cut_markOut = get_timeline_markInOut(project)

    section_cut_ranges["MarkIn"] = full_cut_markIn + 86400
    section_cut_ranges["MarkOut"] = full_cut_markOut + 86400


    return full_cut_markIn, full_cut_markOut

def get_render_presets(project):
    preset_names = project.GetRenderPresets()

    return preset_names


def single_shots_render_settings(project, output_folder, selected_render_preset):
    """Set render settings for individual shots and create render jobs."""
    timeline = get_timeline(project)
    if not timeline:
        print("No current timeline found.") 
        return []

    project.SetCurrentRenderMode(1)
    #render_preset = next(iter(project.GetRenderPresetList()), "DefaultPreset")
    render_preset = project.LoadRenderPreset(selected_render_preset)
    MarkInOut = timeline.GetMarkInOut()
    MarkIn = MarkInOut.get("video", {}).get("in", 0)
    MarkOut = MarkInOut.get("video", {}).get("out", 0)

    render_jobs = []
    for clip in get_clips_from_timeline(project):
        clip_start, clip_end = clip.GetStart(False), clip.GetEnd(False)
        #print(f"Shot {clip.GetName()} start time: {clip_start}, end time: {clip_end}")
        
        clip_start_adjusted = clip_start - 86400
        clip_end_adjusted = clip_end - 86400
        
        
        if clip_start_adjusted >= MarkIn and clip_end_adjusted <= MarkOut:
            
            render_name = f"{clip.GetName()}_{timeline.GetName()}"
            

            project.SetRenderSettings({
                "TargetDir": output_folder,
                "CustomName": render_name,
                "MarkIn": clip_start,
                "MarkOut": clip_end - 1
            })
            render_job = project.AddRenderJob()
            if render_job:
                shot_cut_ranges[render_job] = {
                    "MarkIn": clip_start,
                    "MarkOut": clip_end - 1
            }
                print(f"Added render job for clip: {clip.GetName()}, Job ID: {render_job}, Render Preset: {selected_render_preset}")
                render_jobs.append(render_job)
            else:
                print(f"Failed to add render job for clip: {clip.GetName()}")

    print(f"Created {len(render_jobs)} single shot render jobs")
    return render_jobs


def full_cut_render_settings(project, output_folder, selected_render_preset):
    """Set render settings for full cut and create render job."""

    timeline = get_timeline(project)
    if not timeline:
        print("No current timeline found.") 
        return []

    project.SetCurrentRenderMode(1)
    #render_preset = next(iter(project.GetRenderPresetList()), "DefaultPreset")
    render_preset = project.LoadRenderPreset(selected_render_preset)

    timeline_markers = get_timeline_markers(project)
    for key, value in timeline_markers.items():
        if value.get("color") == "Blue":
            start_frame = key
        elif value.get("color") == "Red":
            end_frame = key


    project_name = project.GetName()
    timeline_name = get_timeline_name(project)
    if not timeline_name:
        return None, None
    
    project.SetRenderSettings({
        "TargetDir": output_folder,
        "CustomName": timeline_name,
        "MarkIn": start_frame,
        "MarkOut": end_frame
    })
    full_cut_render_job = project.AddRenderJob()
    if full_cut_render_job:
        full_cut_ranges[full_cut_render_job] = {
            "MarkIn": start_frame + 86400,
            "MarkOut": end_frame + 86400
        }
        print(f"Added full cut render job {timeline_name}, Job ID: {full_cut_render_job}, Render Preset: {selected_render_preset}")
    else: 
        print("Failed to create full cut render job")
    return full_cut_render_job, timeline_name


def section_render_settings(project, output_folder, selected_render_preset):
    
    timeline = get_timeline(project)
    if not timeline:
        print("No current timeline found.") 
        return []

    project.SetCurrentRenderMode(1)
    #render_preset = next(iter(project.GetRenderPresetList()), "DefaultPreset")
    render_preset = project.LoadRenderPreset(selected_render_preset)

    MarkIn = section_cut_ranges["MarkIn"]
    MarkOut = section_cut_ranges["MarkOut"]
    print(MarkIn, MarkOut)

    project_name = project.GetName()
    timeline_name = get_timeline_name(project)
    if not timeline_name:
        return None, None
    
    project.SetRenderSettings({
        "TargetDir": output_folder,
        "CustomName": timeline_name + "_section",
        "MarkIn": MarkIn,
        "MarkOut": MarkOut
    })
    section_render_job = project.AddRenderJob()
    if section_render_job:
        section_cut_ranges[section_render_job] = {
            "MarkIn": MarkIn,
            "MarkOut": MarkOut
        }
        print(f"Added full cut render job {timeline_name}, Job ID: {section_render_job}, Render Preset: {selected_render_preset}")
    else: 
        print("Failed to create full cut render job")
    return section_render_job


def get_unique_renderJob_name(project, selected_render_preset, output_folder, render_single_shots=True, render_full_cut=True, render_section_cut=True):
    """Ensure render job filenames are unique by checking existing ones and updating if necessary."""
    updated_jobs = []
    if render_single_shots:
        single_shots_render_settings(project, output_folder, selected_render_preset)
    
    if render_full_cut:
        full_cut_render_settings(project, output_folder, selected_render_preset)
    
    if render_section_cut:
        section_render_settings(project, output_folder, selected_render_preset)

    for job in project.GetRenderJobList():
        job_filename = job.get("OutputFilename", "Unknown")
        job_folder = job.get("TargetDir", "Unknown")
        job_id = job.get("JobId", "Unknown")

        if job_id in shot_cut_ranges:
            job_markIn = shot_cut_ranges[job_id]["MarkIn"]
            job_markOut = shot_cut_ranges[job_id]["MarkOut"]
        
        elif job_id in full_cut_ranges:
            job_markIn = full_cut_ranges[job_id]["MarkIn"]
            job_markOut = full_cut_ranges[job_id]["MarkOut"]
            
        else:
            job_markIn = section_cut_ranges.get("MarkIn", 0)
            job_markOut = section_cut_ranges.get("MarkOut", 0)
            

        base_name, ext = os.path.splitext(job_filename)
        new_filename = get_unique_filename(base_name, job_folder, ext.lstrip("."))[1]
        if new_filename != job_filename:
            print(f"Updating job {job_id} filename: {job_filename} to {new_filename} with mark in: {job_markIn} and mark out: {job_markOut}")
            project.DeleteRenderJob(job_id)

            project.SetRenderSettings({
                "TargetDir": job_folder,
                "CustomName": new_filename,
                "MarkIn": job_markIn,
                "MarkOut": job_markOut
            })
            updated_jobs.append(project.AddRenderJob())
        else:
            updated_jobs.append(job_id)
            print(f"Adding job: {job_id}")
    return updated_jobs


def render_jobs(project, selected_render_preset, output_folder: str, render_single_shots=True, render_full_cut=True, render_section_cut=True) -> None:
    """Render all jobs after ensuring unique filenames."""


    get_timeline_marks(project)
    jobs_to_render = get_unique_renderJob_name(
        project,
        selected_render_preset,
        output_folder,
        render_single_shots=render_single_shots,
        render_section_cut=render_section_cut,
        render_full_cut=render_full_cut,
        
    )


    if jobs_to_render:
        print("Rendering current jobs please wait.")
        project.StartRendering(jobs_to_render)


