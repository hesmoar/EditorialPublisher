
import os
import sys
import pprint

#export_directory = #Define your path in here. Example: "C:/Users/username/Desktop/Exported_Timelines"
#TO DO
# Need to determine a name for the render job. 
# Need to see if I can take the path from Kitsu
# Need to connect this with edl exporter so that it runs both, when publishing a cut it exports an edl and 
# updates all the shots in kitsu 


def get_current_project():
    """
    Retrieves the current project from DaVinci Resolve.
    This function uses the DaVinci Resolve API to get the current project
    being worked on. It prints the name of the current project and returns
    the project object.
    Returns:
        object: The current project object from DaVinci Resolve.
    """
    resolve = app.GetResolve()
    projectManager = resolve.GetProjectManager()
    current_project = projectManager.GetCurrentProject()
    project = current_project.GetName()
    #print(project)

    return current_project




def single_shots_render_settings(): 
    """
    Configures and starts a render job in DaVinci Resolve using the first available render preset.
    This function performs the following steps:
    1. Retrieves the current project.
    2. Sets the current render mode to 0.
    3. Retrieves the list of render presets and selects the first preset.
    4. Constructs the output folder path and filename based on the project and timeline names.
    5. Sets the render settings with the target directory and custom filename.
    6. Adds a new render job to the project.
    7. Starts the rendering process for the new render job.
    Returns:
        bool: The result of setting the current render mode.
    """
    project = get_current_project()
    project_renderMode = project.SetCurrentRenderMode(0)
    render_preset_list = project.GetRenderPresetList()
    render_preset = project.GetRenderPresetList()[0]  # Use first preset
    project_name = project.GetName()
    output_folder = r"D:\HecberryStuff\PAINANI STUDIOS\1_Proyectos\Active\1_Animaorquesta\PipeTest\RenderTest"

    timeline_name = project.GetCurrentTimeline().GetName()
    Filename_tmp = project_name + "_" + timeline_name + "_test"
    
    render_folder = project.SetRenderSettings({
        "TargetDir": output_folder,
        "CustomName": Filename_tmp
    })

    single_shots_render_job = project.AddRenderJob()
    print(f"Parameters set for render job for project: {project_name}, render preset: {render_preset}")


    return single_shots_render_job




def full_cut_render_settings():

    project = get_current_project()
    project_renderMode = project.SetCurrentRenderMode(1)
    render_preset_list = project.GetRenderPresetList()
    render_preset = project.GetRenderPresetList()[0]  # Use first preset
    project_name = project.GetName()
    output_folder = r"D:\HecberryStuff\PAINANI STUDIOS\1_Proyectos\Active\1_Animaorquesta\PipeTest\RenderTest"

    timeline_name = project.GetCurrentTimeline().GetName()
    Filename_tmp = project_name + "_" + timeline_name + "_test"
    
    render_folder = project.SetRenderSettings({
        "TargetDir": output_folder,
        "CustomName": Filename_tmp
    })

    full_cut_render_job = project.AddRenderJob()
    print(f"Parameters set for render job for project: {project_name}, render preset: {render_preset}")


    return full_cut_render_job

#single_shots_render_settings()
#full_cut_render_settings()



def render_jobs():
    project = get_current_project()
    single_shot_render_job = single_shots_render_settings()
    full_cut_render_job = full_cut_render_settings()
    project.StartRendering(single_shots_render_settings, full_cut_render_settings)


render_jobs()

