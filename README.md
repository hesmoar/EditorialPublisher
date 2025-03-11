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
1. file management. 
   A. Check for existing files and names 
   B. Creation of folders and files 
   C. Syncronization using Syncthing, 
   D. File Management could maybe work with Prism. 
   E. File management should also be as modular as possible so it can be software agnostic. 
2. update based on a playlist, flag if any of the shots cut length has changed from latest editorial update. (this should also be flagged when publishing in animation or layout or whatever step.)
3. Load latest versions of shots regardless of task. Ask the user if they want any specific tasks 
4. This should be as software agnostic as possible, so also implement other editorial softwares like kdknife 
5. Investigate what would be the input for editorial from storyboard or animatic. Exports from storyboarder or toon boom storyboard. 
6. Add support to transitions, effects and other elements done in multiple tracks by editorial. 
7. Currently Kitsu and OpenTimelineIO services are running on a vm 

## License
This project is licensed under the MIT License.