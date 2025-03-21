# timeline_utils.py
import os
from project_utils import get_current_project

def get_timeline(project):
    """Get the current timeline of the project."""
    timeline = project.GetCurrentTimeline()
    if not timeline:
        print("Error: No current timeline found.")
        return None
    return timeline

def get_timeline_name(project):
    """Get the timeline name prefixed by the project name."""
    timeline = get_timeline(project)
    if timeline:
        return f"{project.GetName()}_{timeline.GetName()}"
    return None

def get_clips_from_timeline(project):
    """Get clips from the current timeline."""
    timeline = get_timeline(project)
    if timeline:
        return timeline.GetItemListInTrack("video", 1)
    return []
