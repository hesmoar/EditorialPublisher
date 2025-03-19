import gazu
import pprint
import json
import opentimelineio as otio
import re
import tkinter as tk
from kitsu_project_context import get_project, select_project
from tkinter import filedialog



regex_pattern = r"(\w+)_(\d{4})-(\d{4})"

def ask_for_file_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select an EDL or OTIO file",
        filetypes=(("EDL files", "*.edl"),("OTIO files", "*.otio"),("All files", "*.*"))
    )
    return file_path

#This file will compare the info from the EDL with the information in Kitsu and update based on that. 

def read_edl(file_path):
    """
    Reads an EDL (Edit Decision List) file and extracts shot information.
    This function reads an EDL file using the OpenTimelineIO (otio) library,
    iterates through the timeline tracks and clips, and extracts shot names
    and their timeframes. The extracted information is returned as a list
    of dictionaries.
    Returns:
        list: A list of dictionaries, each containing:
            - name (str): The name of the shot.
            - timeframe_in (str): The start timecode of the shot.
            - timeframe_out (str): The end timecode of the shot.
    """
    timeline = otio.adapters.read_from_file(file_path)
    edl_shots = []

    for track in timeline.tracks:
        for clip in track:
            if isinstance(clip, otio.schema.Clip):
                clip_name = clip.name
                clip_range = clip.range_in_parent()

                if clip_range:
                    start_time = clip_range.start_time
                    duration = clip_range.duration
                    frame_rate = start_time.rate

                    clip_in = start_time.to_timecode()
                    end_time = start_time + duration - otio.opentime.RationalTime(1, frame_rate)
                    clip_out = end_time.to_timecode()

                    match = re.match(regex_pattern, clip_name)
                    if match:
                        shot_name = match.group(3)
                        edl_shots.append({"name": shot_name, 
                                          "timeframe_in": clip_in, 
                                          "timeframe_out": clip_out
                                          })
                #print(f"Match found for clip {clip_name}")
                    else:
                        print(f"No match found for clip {clip_name}")
    return edl_shots

def read_otio(file_path):
    timeline = otio.adapters.read_from_file(file_path)
    otio_shots = []

    for track in timeline.tracks:
        for clip in track:
            if isinstance(clip, otio.schema.Clip):   # Ensure it's a clip
                clip_timein_source = clip.source_range.start_time
                clip_end_time = clip.source_range.end_time_exclusive() - otio.opentime.RationalTime(1, clip_timein_source.rate)


                
                #one_frame = otio.opentime.RationalTime(1, clip_timein_source.rate)
                #clip_timeout_sum = clip_timein_source + clip_duration - one_frame
                #print(clip_timeout_sum)
                clip_timein = clip_timein_source.to_timecode()
                clip_timeout = clip_end_time.to_timecode()
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
    #pprint.pprint(otio_shots)
    return otio_shots


#This function gets all the shots from a project in kitsu and creates a dictionarywith their name, timeframe_in and timeframe_out keys
def get_project_shots():
    selected_project = select_project()
    project = gazu.project.get_project_by_name(selected_project)
    shots = gazu.shot.all_shots_for_project(project)

    #pprint.pprint(shots)

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

    return kitsu_shots

#This function should take the shots that where a match and have some differences in their timecode and update them in Kitsu
#def update_kitsu():


# This function compares the dictionary coming from the edl and the one from kitsu to see if the shot names are matching. 
def compare_shots(edit_shots, kitsu_shots):

    

    shots_to_update = []

    for shot in edit_shots:
        shot_name = shot.get("name")
        shot_cut_in = shot.get("timeframe_in")
        shot_cut_out = shot.get("timeframe_out")
        

        match_found = False

        for kitsu_shot in kitsu_shots:
            kitsu_shot_name = kitsu_shot.get("name")
            kitsu_shot_cut_in = kitsu_shot.get("timeframe_in")
            kitsu_shot_cut_out = kitsu_shot.get("timeframe_out")
            kitsu_shot_id = kitsu_shot.get("id")


            if shot_name == kitsu_shot_name:
                if shot_cut_in != kitsu_shot.get("timeframe_in"):
                    print(f"Cut in for shot {shot_name} is different in Kitsu")
                    shots_to_update.append({
                        "name": shot_name,
                        "timeframe_in": shot_cut_in,
                        "timeframe_out": shot_cut_out,
                        "id": kitsu_shot_id
                        })
                    print(f"Shot {shot_name} will be updated in Kitsu")

                    match_found = True
                if shot_cut_out != kitsu_shot.get("timeframe_out"):
                    print(f"Cut out for shot {shot_name} is different in Kitsu")
                    shots_to_update.append({
                        "name": shot_name,
                        "timeframe_in": shot_cut_in,
                        "timeframe_out": shot_cut_out,
                        "id": kitsu_shot_id
                        })
                    match_found = True

    return shots_to_update


def update_kitsu():
    kitsu_shots = get_project_shots()
    file_path = ask_for_file_path()

    if file_path.endswith('.edl'):
        edit_shots = read_edl(file_path)
    elif file_path.endswith('.otio'):
        edit_shots = read_otio(file_path)
    else:
        print("Unsupported file format")
        return

    shots_to_update = compare_shots(edit_shots, kitsu_shots)

    if not shots_to_update:
        print("No shots to update. Everything is up to date.")
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



update_kitsu()
