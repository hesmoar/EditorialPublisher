# 🎬 Editorial Publisher
THIS IS A WORK IN PROGRESS!!!

A modular toolset for exporting and rendering editorial timelines in **DaVinci Resolve**, and updating metadata in Kitsu. This project allows you to streamline the editorial process tracking by exporting OTIO files, and rendering shot-based clips and full cuts automatically and publishing previews into the project management software (**Kitsu**). 

![Tool Speed Run](https://github.com/hesmoar/EditorialPublisher/blob/master/readme_resources/EditorialPublisher_SpeedRun.gif)
---

## 🚀 **Features**

✅ Export OTIO files from DaVinci Resolve timelines.\
✅ Render individual shots, section and/or full cuts.\
✅ Functionality to publish (or not) elements into Kitsu server.\
✅ Modular and extensible design for easy customization.\
✅ Easy to read GUI for user input.\


---

## **Requirements**

1. Python 3.7 - 3.10
2. DaVinci Resolve
3. OTIO
4. Kitsu Server


## ⚙️ **Installation**
This setup is assuming you have a kitsu server already set up or not planning to use Kitsu functionality 
Kitsu setup guide: https://zou.cg-wire.com/#

1. **Clone the Repository**

```bash
git clone https://github.com/hesmoar/EditorialPublisher.git
cd EditorialPublisher
```

2. **Set Up Environment Variables**

- Add the following variables:

```
PIPE_SCRIPTS_PATH= Path where you store the repository
KITSU_URL= URL to your kitsu site
KITSU_EMAIL= Your email to access Kitsu
KITSU_PASSWORD= Your Kitsu password 
```
- Make sure Da Vinci Resolve scripting environment is properly setup you can refer to this documentaion: https://resolvedevdoc.readthedocs.io/en/latest/API_intro.html

3. **Install Required Dependencies**

- If you’re using a virtual environment:

```bash
pip install -r requirements.txt
```
4. **Move main.py into the path where your Da Vinci Resolve stores the scripts**
   - Usually in the following path:
   ```bash
   C:\ProgramData\Blackmagic Design\DaVinci Resolve\Fusion\Scripts
   ```
5. **Adjust Script values to your own project and pipeline needs**
   - There are certain values that are currently specific for my project and pipeline setup but you can modify as needed. 
      - Regex pattern for shot names found at the start of **kitsu_editorial_publisher.py**
      - Render Preset selection, this is currently set to the first preset. You can find this inside **render_utils.py** in the following functions:
         - single_shots_render_settings
         - full_cut_render_settings
      - Kitsu custom field "timeframe_in" and "timeframe_out" you can change this to whatever field you want to use inside of kitsu. You can find this in **kitsu_editorial_publisher.py**


## 💡 **Usage**

1. **Prepare DaVinci Resolve**
   - Open DaVinci Resolve.
   - Load your project.
   - In the edit page lets set 2 timeline markers (these will determine the start and end frame of your full cut):
      - Blue marker: on the start of your cut
      - Red marker: on the end of your cut 
   - In the Deliver page set your mark in and mark out


2. **Run the Script**
   - In DaVinci Resolve got to the Workspace menu
   - Select Console, this will bring up the console, make sure to select Py3
   - Go to the Workspace menu again
   - Select Scripts
   - Depending on where you saved the script it will appear on the menu 
   - Click on the script and it will begin to run

3. **Select Output Folders**

- A GUI will appear, prompting you to:
   - Directory Selection:
      - Select the **Render Output Folder**. (This is where you want to save your renders)
      - Select the **EDL/OTIO Export Folder**. (This is where you want to save your EDL file)
   - Render Options:
      - Select the renders you need from the checkboxes
         - Single shots
         - Section Render cut
         - Full Cut 
      - Select the render preset (Based on the render presets in davinci)
   - Export Options:
      - Export OTIO: Check if you want to export an OTIO file of your current timeline (This is the file that will be used to update cut items in Kitsu metadata)
      - Upload to Kitsu: Check if you want to upload renders and update metadata in Kitsu server
         - Select Kitsu Project: Available projects in your kitsu server
         - Select Kitsu Edit: Available edits inside the selected project (This is were the full cut will be published to)
         - Select Kitsu Edit Task: Available tasks for the selected edit (This is were the full cut will be published to)
   - Preview Comment:
      - Description field: This is a text field which the contents will be used as the comment published for the preview in Kitsu, this applies for single shots and full cut. 

   - **Automated Processing**
   - The script will:
     - Export the OTIO file to the selected folder
     - Delete existing render jobs in the DaVinci project.
     - Apply rendering settings by using the selected values and preset in the GUI.
     - Ensure files have a unique name including the version suffix (v001)
     - Render the new render jobs
     - Compare the metadata from the OTIO file with the information in Kitsu and update if necessary
     - Publish previews of the single shots into their matching shot in Kitsu using the description as a comment
     - Publish previews of the full cut into the select edit task. 

## 🗺️ Roadmap
1. [ ] Add file management functionality
   * Creation of folders and move files
   * Follow a specific File tree structure

2. [ ] Add support for multiple tracks (Currently only tested with 1 track)

3. [ ] Add support for effects and transitions. 

4. [ ] Implement other editorial software
   * [ ] OpenShot
   * [ ] Kdenlive
   * [ ] Adobe Premiere
   * [ ] Avid

5. [ ] Implement other project tracking softwares
   * [ ] Shotgrid/Shotgun/Flow
   * [ ] FTrack

## 🛠️ **Contributing**

1. **Fork the repository**.
2. Create a new branch for your feature or bugfix:

```bash
git checkout -b feature-name
```

3. Make your changes and commit them:

```bash
git commit -m "Add new feature"
```

4. Push the branch:

```bash
git push origin feature-name
```

5. Open a **pull request**.

---

## 🐛 **Issues**

If you encounter any issues or have feature suggestions, feel free to [open an issue](https://github.com/hesmoar/EditorialPublisher/issues).

---

## 📄 **License**

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 👥 **Author**

**Hector E.**\
[GitHub](https://github.com/hesmoar)\
[LinkedIn](https://www.linkedin.com/in/hesmoar)



