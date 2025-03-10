# Editorial Publisher

THIS IS STILL A WORK IN PROGRESS

## Overview
The Editorial Publisher is a Python script designed to export timelines from DaVinci Resolve in EDL (Edit Decision List) format. This tool simplifies the process of exporting timelines for further editing or archiving.

## Features
- Generates unique filenames for exported EDL files.
- Validates the existence of timelines and export directories.
- Handles errors during the export process.

## Installation
1. Ensure you have Python installed on your system.
2. Clone the repository or download the script.
3. Install the required dependencies using the command:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Open DaVinci Resolve and load your project.
2. Set the `export_directory` variable in `DaVinci_edl_Exporter.py` to your desired export path.
3. Run the script to export the current timeline as an EDL file.

## License
This project is licensed under the MIT License.