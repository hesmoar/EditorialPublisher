# timeline_utils.py
import os
from project_utils import get_current_project
import pprint

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

def get_timeline_markers(project):
    timeline = get_timeline(project)
    if timeline:
        pprint.pprint(timeline.GetMarkers())
        return timeline.GetMarkers()
    return []

def get_timeline_markInOut(project):
    """Get and store the full cut frame range from the timeline."""

    timeline = get_timeline(project)
    if not timeline:
        print("No current timeline found.") 
        return []

    MarkInOut = timeline.GetMarkInOut()
    full_cut_markIn = MarkInOut.get("video", {}).get("in", 0)
    full_cut_markOut = MarkInOut.get("video", {}).get("out", 0)


    return full_cut_markIn, full_cut_markOut