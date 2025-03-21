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

## ⚙️ **Installation**

1. **Clone the Repository**

```bash
git clone https://github.com/hesmoar/EditorialPublisher.git
cd EditorialPublisher
```

2. **Set Up Environment Variables**

- Create a `.env` file at the root of the project.
- Add the following variables:

```
PIPE_SCRIPTS_PATH= **Path where you store the scripts**
```

3. **Install Required Dependencies**

- If you’re using a virtual environment:

```bash
pip install -r requirements.txt
```

- If you want to run the GUI:

```bash
pip install tk
```

4. **Add the DaVinci Resolve Scripting Path**

- Add the Resolve scripting path to your `PYTHONPATH` or use a `.env` file to point to it.

---

## 🛠️ **Usage**

1. **Run the Script**

```bash
python main.py
```

2. **Select Output Folders**

- A GUI will appear, prompting you to:
  - Select the **Render Output Folder**.
  - Select the **EDL/OTIO Export Folder**.

3. **DaVinci Resolve Integration**

- The script will automatically:
  - Load the current Resolve project.
  - Export EDL/OTIO files.
  - Render individual shots and the full cut.
  - Save the rendered clips and EDLs to the selected folders.

---

## 🌐 **Environment Variables**

The project uses environment variables to configure paths dynamically:

- `PIPE_SCRIPTS`: Path to your script modules.
  - Example: `D:\HecberryStuff\Dev\BetweenStudiosTools`
- `PYTHONPATH`: Add DaVinci Resolve’s scripting path if needed.

---

## 💡 **Example Workflow**

1. **Prepare DaVinci Resolve**
   - Open DaVinci Resolve.
   - Load your project.
2. **Run the Script**

```bash
python main.py
```

3. **Select Folders**
   - Choose folders for EDL/OTIO export and rendered clips.
4. **Automated Processing**
   - The script will:
     - Export the EDL and OTIO files.
     - Delete existing render jobs.
     - Apply rendering settings.
     - Render individual shots or the full cut.
5. **Review the Output**
   - EDLs and OTIO files will be saved in the export folder.
   - Rendered clips will be saved in the output folder.

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
[LinkedIn](https://www.linkedin.com/in/your-profile)



## Roadmap
1. [ ] Single shot render files should follow the naming convention stablished for the project version entity.
   * [x] Done in standalone version
   * [ ] Add to modular version

2. [x] Connect process of edl export and rendering
   * Done in the standalone version

3. [ ] Add button or script to resolve to start the process from inside

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
