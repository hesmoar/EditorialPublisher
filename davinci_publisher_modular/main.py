from project_utils import get_current_project, delete_existing_jobs
from file_utils import export_edl
from render_utils import render_jobs, single_shots_render_settings, full_cut_render_settings

EXPORT_DIRECTORY = r"D:\HecberryStuff\PAINANI STUDIOS\1_Proyectos\Active\1_Animaorquesta\PipeTest"
OUTPUT_FOLDER = r"D:\HecberryStuff\PAINANI STUDIOS\1_Proyectos\Active\1_Animaorquesta\PipeTest\RenderTest\Clips"

if __name__ == "__main__":
    project = get_current_project(app)
    if project:
        print(f"Succesfully loaded the get current project script: {project.GetName()}")
        delete_existing_jobs(project)
        export_edl(project, EXPORT_DIRECTORY)
        render_jobs(project)