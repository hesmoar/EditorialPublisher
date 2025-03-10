import KitsuAuth
import gazu
import pprint
import json
import opentimelineio as otio
import re


project_name = "AnimaOrquesta_Test"
test_edl = r"D:\HecberryStuff\PAINANI STUDIOS\1_Proyectos\Active\1_Animaorquesta\PipeTest\AO_PipeTest_A_v009.edl"

#regex_pattern = r"(AO)_(\d{4})-(\d{4})"
regex_pattern = r"(\w+)_(\d{4})-(\d{4})"


#This file will compare the info from the EDL with the information in Kitsu and update based on that. 

def read_edl():
    timeline = otio.adapters.read_from_file(test_edl)
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


 
def get_project():
    active_projects = gazu.project.all_open_projects()
    selected_project = gazu.project.get_project_by_name(project_name)

    return active_projects


def select_project():
    projects_to_pick = get_project()
    project_names = [project.get("name") for project in projects_to_pick]
    print(project_names)

    print("Please select an active project from the list:")
    for idx, project in enumerate(project_names, start=1):
        print(f"{idx}. {project}")
    
    # Request the user's choice
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(project_names):
                return project_names[choice - 1]  # Return the selected option
            else:
                print("Invalid choice. Please select a valid number from the list.")
        except ValueError:
            print("Please enter a valid number.")

"""
def get_project():

    #selected_project = gazu.project.get_project_by_name(project_name)
    #project_code = selected_project.get("code")
    active_projects = gazu.project.all_open_projects()
    active_projects_names = []
    for project in active_projects:
        project_name = (project.get("name"))
        active_projects_names.append(project_name)

    return active_projects_names



"""

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
def compare_shots():
    kitsu_shots = get_project_shots()
    edl_shots = read_edl()
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


def update_kitsu():
    #project = get_project()
    shots_to_update = compare_shots()
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


#get_project_shots()
read_edl()
#get_project()
#selected_project = select_project()
#print(f"Selected project: {selected_project}")
#update_kitsu()