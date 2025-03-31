# project_utils.py
import sys


def get_current_project(app):
    """Get the current project from the app."""
    resolve = app.GetResolve()
    projectManager = resolve.GetProjectManager()
    project = projectManager.GetCurrentProject()

    if not project:
        print("Error: No current project found.")
        return None
    return project

def delete_existing_jobs(project):
    """Delete all existing render jobs."""
    if project:
        project.DeleteAllRenderJobs()


