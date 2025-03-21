import os
from timeline_utils import get_timeline, get_clips_from_timeline, get_timeline_name
from file_utils import get_unique_filename
from project_utils import get_current_project


def single_shots_render_settings(project, output_folder):
    """Set render settings for individual shots and create render jobs."""
    timeline = get_timeline(project)
    if not timeline:
        print("No current timeline found.") 
        return []

    project.SetCurrentRenderMode(1)
    render_preset = next(iter(project.GetRenderPresetList()), "DefaultPreset")
    MarkInOut = timeline.GetMarkInOut()
    MarkIn = MarkInOut.get("video", {}).get("in", 0)
    MarkOut = MarkInOut.get("video", {}).get("out", 0)

    render_jobs = []
    for clip in get_clips_from_timeline(project):
        clip_start, clip_end = clip.GetSourceStartFrame(), clip.GetSourceEndFrame()
        if clip_start >= MarkIn and clip_end <= MarkOut:
            render_name = f"{clip.GetName()}_{timeline.GetName()}"
            project.SetRenderSettings({
                "TargetDir": output_folder,
                "CustomName": render_name,
                "MarkIn": clip_start,
                "MarkOut": clip_end
            })
            render_job = project.AddRenderJob()
            if render_job:
                print(f"Added render job for clip: {clip.GetName()}")
                render_jobs.append(render_job)
            else:
                print(f"Failed to add render job for clip: {clip.GetName()}")

    print(f"Created {len(render_jobs)} shot render jobs (preset: {render_preset})")
    return render_jobs

def full_cut_render_settings(project, output_folder):
    """Set render settings for full cut and create render job."""
    project.SetCurrentRenderMode(1)
    render_preset = next(iter(project.GetRenderPresetList()), "DefaultPreset")
    project_name = project.GetName()
    timeline_name = get_timeline_name(project)
    if not timeline_name:
        return None, None
    
    project.SetRenderSettings({
        "TargetDir": output_folder,
        "CustomName": timeline_name
    })
    full_cut_render_job = project.AddRenderJob()
    if full_cut_render_job:
        print(f"Created full cut render job (preset: {render_preset})")
    else: 
        print("Failed to create full cut render job")
    return full_cut_render_job, timeline_name

def get_unique_renderJob_name(project, output_folder):
    """Ensure render job filenames are unique by checking existing ones and updating if necessary."""
    updated_jobs = []
    single_shots_render_settings(project, output_folder)
    full_cut_render_settings(project, output_folder)
    for job in project.GetRenderJobList():
        job_filename = job.get("OutputFilename", "Unknown")
        job_folder = job.get("TargetDir", "Unknown")
        job_id = job.get("JobId", "Unknown")

        base_name, ext = os.path.splitext(job_filename)
        new_filename = get_unique_filename(base_name, job_folder, ext.lstrip("."))[1]
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

def render_jobs(project, output_folder):
    """Render all jobs after ensuring unique filenames."""
    jobs_to_render = get_unique_renderJob_name(project, output_folder)
    if jobs_to_render:
        print("Rendering current jobs please wait.")
        project.StartRendering(jobs_to_render)


