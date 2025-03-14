
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

