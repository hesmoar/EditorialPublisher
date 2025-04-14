import gazu
import pprint
import json
import opentimelineio as otio
import re
import os
from kitsu_project_context import select_project, get_project
from render_utils import renders_to_publish



regex_pattern = r"(\w+)_(\d{4})-(\d{4})"
selected_project_shots = []


def read_edl(file_path):

    timeline = otio.adapters.read_from_file(file_path)
    edl_shots = []

    for track in timeline.tracks:
        for clip in track:
            clip_name = clip.name
            clip_range = clip.range_in_parent()
            clip_in = clip_range.start_time.to_timecode()
            clip_out = clip_range.end_time_inclusive().to_timecode()

            match = re.match(regex_pattern, clip_name)
            if match:
                shot_name = match.group(3)
                edl_shots.append({"name": shot_name, 
                                  "timeframe_in": clip_in, 
                                  "timeframe_out": clip_out
                                  })
                print(f"Match found for clip {clip_name}")
            else:
                print(f"No match found for clip {clip_name}")
    return edl_shots


def read_otio(file_path):
    timeline = otio.adapters.read_from_file(file_path)
    otio_shots = []

    for track in timeline.tracks:
        for clip in track:
            if isinstance(clip, otio.schema.Clip):   # Ensure it's a clip
                clip_timein = clip.source_range.start_time.to_timecode()
                clip_timeout = clip.source_range.duration.to_timecode()
                print(f"Clip: {clip.name}, Start Time: {clip_timein}, Duration: {clip_timeout}")

                match = re.match(regex_pattern, clip.name)
                if match:
                    shot_name = match.group(3)
                    otio_shots.append({"name": shot_name,
                                       "timeframe_in": clip_timein,
                                       "timeframe_out": clip_timeout
                                       })
                else:
                    print(f"No match found for clip {clip.name}")
    return otio_shots


def get_project_shots(project_name):
    
    #selected_project = select_project()
    selected_project = project_name

    project = gazu.project.get_project_by_name(selected_project)
    shots = gazu.shot.all_shots_for_project(project)

    kitsu_shots = []
    for shot in shots:
        shot_name = shot.get("name")
        shot_frames = shot.get("nb_frames")
        shot_data_info = shot.get("data")
        shot_time_in = shot_data_info.get("timeframe_in")
        shot_time_out = shot_data_info.get("timeframe_out")
        shot_id = shot.get("id")

        kitsu_shots.append({"name": shot_name,
                            "timeframe_in": shot_time_in, 
                            "timeframe_out": shot_time_out, 
                            "id": shot_id})
        selected_project_shots.append(shot)

    return kitsu_shots


def compare_shots(file_path, project_name):
    #kitsu_shots = get_project_shots()
    kitsu_shots = get_project_shots(project_name) # I added this line for testing
    edl_shots = read_edl(file_path)
    shots_to_update = []

    for edl_shot in edl_shots:
        edl_shot_name = edl_shot.get("name")
        edl_shot_cut_in = edl_shot.get("timeframe_in")
        edl_shot_cut_out = edl_shot.get("timeframe_out")
        

        match_found = False

        for kitsu_shot in kitsu_shots:
            kitsu_shot_name = kitsu_shot.get("name")
            kitsu_shot_cut_in = kitsu_shot.get("timeframe_in")
            kitsu_shot_cut_out = kitsu_shot.get("timeframe_out")
            kitsu_shot_id = kitsu_shot.get("id")


            if edl_shot_name == kitsu_shot_name:
                if edl_shot_cut_in != kitsu_shot.get("timeframe_in"):
                    shots_to_update.append({
                        "name": edl_shot_name,
                        "timeframe_in": edl_shot_cut_in,
                        "timeframe_out": edl_shot_cut_out,
                        "id": kitsu_shot_id
                        })
                    print(f"Shot {edl_shot_name} will be updated in Kitsu")

                    match_found = True
                if edl_shot_cut_out != kitsu_shot.get("timeframe_out"):
                    print(f"Cut out for shot {edl_shot_name} is different in Kitsu")
                    shots_to_update.append({
                        "name": edl_shot_name,
                        "timeframe_in": edl_shot_cut_in,
                        "timeframe_out": edl_shot_cut_out,
                        "id": kitsu_shot_id
                        })
                    match_found = True

    return shots_to_update

def get_review_status():
    return next((status for status in gazu.task.all_task_statuses() if status.get("short_name") == 'wfa'), None)


def files_to_publish(description):

    pending_status = get_review_status()
    published_files = renders_to_publish
    kitsu_shots = selected_project_shots


    for file in published_files:
        filename = os.path.basename(file)
        match = re.search(regex_pattern, filename)
        print(f"These are the filenames {filename}")

        if match:
            shot_name_from_file = match.group(3)

            shot = next((s for s in kitsu_shots if s.get("name") == shot_name_from_file), None)

            if shot:

                #print(f"Found the perfect match on render {shot_name_from_file} and kitsu {shot.get("name")}")
                shot_task = gazu.task.all_tasks_for_shot(shot)

                for shottask in shot_task:
                    if shottask.get("task_type_name") == "Storyboard": # This should ideally be determined by the timeline name
                        #print(f"THIS IS THE FILE PATH: {file}")
                        published_preview = gazu.task.publish_preview(task=shottask, 
                        task_status=pending_status, 
                        comment=description,
                        preview_file_path=file
                        )
                        pprint.pprint(published_preview)

                        data = {
                            "path": file
                        }

                        gazu.files.update_preview(published_preview[1], data)


def update_kitsu(file_path, project_name):
    shots_to_update = compare_shots(file_path, project_name)

    if file_path.endswith('.edl'):
        edl_shots = read_edl(file_path)
    elif file_path.endswith('.otio'):
        edl_shots = read_otio(file_path)
    else:
        print("Unsupported file format")
        return

    if not shots_to_update:
        print("No shots timecode change detected. Everything is up to date.")
        return

    for shot in shots_to_update:
        shot_name = shot.get("name")
        shot_id = shot.get("id")
        shot_data = {
            "timeframe_in": shot.get("timeframe_in"),
            "timeframe_out": shot.get("timeframe_out")
        }
        try:
            print(f"Updating shot {shot_name}, SHOT ID: {shot_id} in Kitsu")
            pprint.pprint(f"Shot data: {shot_data}")
            kitsu_shot = gazu.shot.get_shot(shot_id)
            if not kitsu_shot:
                print(f"Shot {shot_name} not found in Kitsu. Skipping update...")
                continue
            if not isinstance(shot_data, dict):
                print(f"Shot data for {shot_name} is not a dictionary. Skipping update...")
                continue
            gazu.shot.update_shot_data(shot_id, shot_data)
            print(f"Shot {shot_name} updated successfully")
        except Exception as e:
            print(f"Failed to update shot {shot_name} in Kitsu: {e}")




