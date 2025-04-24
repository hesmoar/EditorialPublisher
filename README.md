# 🎬 Editorial Publisher

A modular toolset for exporting and rendering editorial timelines in **DaVinci Resolve**, and updating metadata in Kitsu. This project allows you to streamline the editorial process by exporting EDLs, OTIO files, and rendering shot-based clips and full cuts automatically.

---

## 🚀 **Features**

✅ Export EDL and OTIO files from DaVinci Resolve timelines.\
✅ Render individual shots and/or full cuts.\
✅ Modular and extensible design for easy customization.\
✅ Folder selection via GUI for flexible output locations.\
✅ Error handling and logging for smooth execution.

---

## **Requirements**

1. Python 3.7 - 3.10
2. DaVinci Resolve
3. OTIO


## ⚙️ **Installation**


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
   - In the Deliver page set your mark in and mark out


2. **Run the Script**
   - In DaVinci Resolve got to the Workspace menu
   - Select Console, this will bring up the console, make sure to select Py3
   - Go to the Workspace menu again
   - Select Scripts
   - Depending on where you saved the script it will appear on the menu, 
   - Click on the script and it will begin to run

3. **Select Output Folders**

- A GUI will appear, prompting you to:
  - Select the **Render Output Folder**. (This is where you want to save your renders)
  - Select the **EDL/OTIO Export Folder**. (This is where you want to save your EDL file)

   - **Automated Processing**
   - The script will:
     - Export the EDL file to the selected folder
     - Delete existing render jobs in the DaVinci project.
     - Apply rendering settings by using the first preset. (you can change this in the "render_utils.py" file)
     - Render individual shots and the full cut.

4. **Obtaining data from Kitsu**
   - A GUI will appear, prompting you to:
      - Select an active project from your Kitsu site

      - **Automated Processing**
      - The script will:
         - Look into the Kitsu database for the project you selected.
         - Retrieve shots and compare the names of the shots with the ones in your edl file
         - Find matching names and find differences in the timeframe_in and timeframe_out custom field
         - Where differences are found it will update the metadata based on the recently exported edl.
---

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

**Hector S.**\
[GitHub](https://github.com/hesmoar)\
[LinkedIn](https://www.linkedin.com/in/hesmoar)



## Roadmap
1. [x] Single shot render files should follow the naming convention stablished for the project version entity.
   * [x] Done in standalone version
   * [x] Add to modular version

2. [x] Connect process of edl export and rendering
   * Done in the standalone version

3. [x] Add button or script to resolve to start the process from inside

4. [ ] Load versions from Kitsu into Resolve timeline
   * [ ] Latest versions for each shot
   * [ ] Based on a Playlist
   * [ ] Ask user for specifc tasks
   * [ ] Flag user if any shot has changed from the latest editorial cut 

5. [ ] File management. 
   * [ ] Check for existing files and names based on a specific directory structure
   * [ ] Creation of folders and files 
   * [ ] Syncronization setup using syncthing or other file management systems 
   * File Management could maybe work with Prism. 
   * [ ] File management should also be as modular as possible so it can be software agnostic. 

6. [ ] Add support to transitions, effects and other elements done in multiple tracks by editorial.

7. [ ] Add support to run process in a render farm to avoid using the user computer

8. [ ] Implement other editorial software
   * [ ] OpenShot
   * [ ] Kdenlive
   * [ ] Adobe Premiere
   * [ ] Avid

9. [ ] Investigate what would be the input for editorial from storyboard or animatic. Exports from storyboarder or toon boom storyboard. 
