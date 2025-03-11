# Editorial Publisher

THIS IS STILL A WORK IN PROGRESS

## Overview
The Editorial Publisher is a Python tool designed to automate the publication process for editorial department, by exporting timelines from DaVinci Resolve in EDL (Edit Decision List) format and render the full cut and single shots, updating the information stored in Kitsu (project manager).

## Features
- `DaVinci_edl_Exporter.py`
   - Generates unique filenames for exported EDL files.
   - Validates the existence of timelines and export directories.
   - Handles errors during the export process.
- `DaVinciRendering.py`
   - Creates 2 render jobs: one with the full cut and another for single shots.
- `KitsuAuth.py`
   - Logs into Kitsu server based on the environment variables.
- `kitsuEditorial_publisher.py`
   - Reads a given EDL using OTIO and stores the data from the shot and its cut in and cut out values.
   - Retrieves data from Kitsu shots.
   - Compares data from both EDL and Kitsu and updates the data in Kitsu if there are differences with the EDL.
- `project_context.py`
   - Retrieves projects from Kitsu and allows the user to select one.
- `kitsu_update.py`
   - Updates shot information in Kitsu based on the comparison results.


## Installation
IN CONSTRUCTION

## Usage
IN CONSTRUCTION

## Roadmap
1. [ ] Load versions from Kitsu into Resolve timeline
   * [ ] Latest versions for each shot
   * [ ] Based on a Playlist
   * [ ] Ask user for specifc tasks
   * [ ] Flag user if any shot has changed from the latest editorial cut 

2. [ ] File management. 
   * [ ] Check for existing files and names based on a specific directory structure
   * [ ] Creation of folders and files 
   * [ ] Syncronization setup using syncthing or other file management systems 
   * File Management could maybe work with Prism. 
   * [ ] File management should also be as modular as possible so it can be software agnostic. 

3. [ ] Add support to transitions, effects and other elements done in multiple tracks by editorial.

4. [ ] Implement other editorial software
   * [ ] 

5. [ ] Investigate what would be the input for editorial from storyboard or animatic. Exports from storyboarder or toon boom storyboard. 

 

6. [x] Currently Kitsu and OpenTimelineIO services are running on a vm 

## License
This project is licensed under the MIT License.