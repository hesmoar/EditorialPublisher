import sys
import os
import pprint
import tkinter as tk
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QCheckBox, QRadioButton, QButtonGroup, QFileDialog, QHBoxLayout, QGroupBox, QFrame, QSpacerItem, QSizePolicy, QComboBox, QTextEdit
)
from PySide6.QtCore import Qt
from render_utils import get_render_presets




class ResolvePublisherGUI(QMainWindow):
    """GUI for selecting export and render options"""

    def on_kitsu_checkbox_changed(self, state):
        """Triggered when Upload to Kitsu checkbox is toggled."""
        if state == 2: # If checked
            try:
                import gazu
                from kitsu_auth import connect_to_kitsu


                print("Logging into Kitsu and fetching projects...")
                connect_to_kitsu()
                projects = gazu.project.all_open_projects()

                self.projects_dropdown.clear()
                self.projects_dropdown.addItem("Select Kitsu Project")
                self.project_map = {}

                for project in projects:
                    name = project["name"]
                    self.projects_dropdown.addItem(name)
                    self.project_map[name] = project

                print(f"Loaded {len(projects)} projects from Kitsu.")
            except Exception as e:
                print(f"Failed to fetch Kitsu projects: {e}")
        else:

            self.projects_dropdown.clear()
            self.projects_dropdown.addItem("Kitsu not enabled")


    def __init__(self, presets):
        super().__init__()
        self.setWindowTitle("Editorial Publisher Settings")
        self.setGeometry(300, 200, 650, 450)

        # Add Icon to the window 
        #self.setWindowIcon(QIcon())

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Directory Selection

        dir_group = QGroupBox("Directory Selection")
        dir_layout = QVBoxLayout(dir_group)

        self.export_dir_label = QLabel("OTIO export Directory: Not Selected")
        self.export_dir_button = QPushButton("Select OTIO export Directory")
        self.export_dir_button.clicked.connect(self.select_export_dir)

        self.output_dir_label = QLabel("Render Output Directory: Not Selected")
        self.output_dir_button = QPushButton("Select Render Output Directory")
        self.output_dir_button.clicked.connect(self.select_output_dir)

        dir_layout.addWidget(self.export_dir_label)
        dir_layout.addWidget(self.export_dir_button)
        dir_layout.addWidget(self.output_dir_label)
        dir_layout.addWidget(self.output_dir_button)

        # Render Options
        render_group = QGroupBox("Render Options")
        render_layout = QHBoxLayout(render_group)

        # Left Column
        left_layout = QVBoxLayout()
        self.render_group = QButtonGroup()
        self.single_shot_checkbox = QCheckBox("Single Shots")
        self.section_cut_checkbox = QCheckBox("Section Render cut")
        self.full_cut_checkbox = QCheckBox("Full Cut")
        left_layout.addWidget(self.single_shot_checkbox)
        left_layout.addWidget(self.section_cut_checkbox)
        left_layout.addWidget(self.full_cut_checkbox)

        self.single_shot_checkbox.setChecked(True) # Default selections
        self.full_cut_checkbox.setChecked(True)

        # Right Column
        right_layout = QVBoxLayout()
        self.preset_dropdown = QComboBox()
        self.preset_dropdown.addItems(presets)
        right_layout.addWidget(QLabel("Select Render Preset:"))
        right_layout.addWidget(self.preset_dropdown)

        #self.update_preset_dropdown()


        render_layout.addLayout(left_layout)
        render_layout.addLayout(right_layout)

        # Checkboxes
        checkbox_group = QGroupBox("Export Options")
        checkbox_layout = QHBoxLayout(checkbox_group)

        checkbox_left_layout = QVBoxLayout()
        self.checkbox_group = QButtonGroup()
        self.export_otio_checkbox = QCheckBox("Export OTIO")
        self.upload_kitsu_checkbox = QCheckBox("Upload to Kitsu")
        self.upload_kitsu_checkbox.stateChanged.connect(self.on_kitsu_checkbox_changed)
        checkbox_left_layout.addWidget(self.export_otio_checkbox)
        checkbox_left_layout.addWidget(self.upload_kitsu_checkbox)

        self.export_otio_checkbox.setChecked(True)
        self.upload_kitsu_checkbox.setChecked(False)

        checkbox_right_layout = QVBoxLayout()
        self.projects_dropdown = QComboBox()
        self.projects_dropdown.addItems(["Select Kitsu Project"])
        self.projects_dropdown.currentIndexChanged.connect(self.on_project_selected)
        checkbox_right_layout.addWidget(QLabel("Select Kitsu Project:"))
        checkbox_right_layout.addWidget(self.projects_dropdown)
        
        self.edits_dropdown = QComboBox()
        self.edits_dropdown.addItems(["Select Kitsu Edit"])
        self.edits_dropdown.currentIndexChanged.connect(self.on_edit_selected)
        checkbox_right_layout.addWidget(QLabel("Select Kitsu Edit:"))
        checkbox_right_layout.addWidget(self.edits_dropdown)

        self.edit_tasks_dropdown = QComboBox()
        self.edit_tasks_dropdown.addItems(["Select Kitsu Edit Task"])
        checkbox_right_layout.addWidget(QLabel("Select Kitsu Edit Task:"))
        checkbox_right_layout.addWidget(self.edit_tasks_dropdown)


        checkbox_layout.addLayout(checkbox_left_layout)
        checkbox_layout.addLayout(checkbox_right_layout)


        # Comment
        comment_group = QGroupBox("Preview Comment")
        comment_layout = QVBoxLayout(comment_group)

        self.comment_label = QLabel("Add a description for the shot")

        self.comment = QTextEdit(self)

        comment_layout.addWidget(self.comment_label)
        comment_layout.addWidget(self.comment)


        # Buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_process)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_and_exit)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.cancel_button)


        self.export_dir = ""
        self.output_dir = ""
        self.selections = {}

        # Adding to main layout
        main_layout.addWidget(dir_group)
        main_layout.addWidget(render_group)
        main_layout.addWidget(checkbox_group)
        main_layout.addWidget(comment_group)

        # Add some spacing
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        main_layout.addLayout(button_layout)


        # Apply stylesheet for a modern look
        self.apply_stylesheet()


    # ------------------------ STYLESHEET ------------------------
    def apply_stylesheet(self):
        """Apply stylesheet for modern look"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e22;
                color: #f0f0f0;
            }
            
            QLabel {
                font-size: 14px;
                color: white;
            }

            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #f0f0f0;
                border: 1px solid #555;
                border-radius: 8px;
                margin-top: 15px;
                padding: 15px;
            }

            QPushButton {
                background-color: #28282e;
                color: white;
                font-size: 14px;
                border-radius: 5px;
                padding: 8px 12px;
            }

            QPushButton:hover {
                background-color: #737373;
            }

            QRadioButton, QCheckBox {
                font-size: 14px;
                color: white;
            }

            QPushButton:disabled {
                background-color: #555;
                color: #aaa;
            }

            QLineEdit, QTextEdit {
                background-color: #333;
                color: white;
                border: 1px solid #555;
            }
            
        """)

    #def update_preset_dropdown(self):
    #    presets = render_presets
    #    self.preset_dropdown.clear()
    #    self.preset_dropdown.addItems(presets)

    # Select directory functions
    def select_export_dir(self):
        """Select the export directory."""
        dir_name = QFileDialog.getExistingDirectory(self, "Select OTIO Export Directory")
        if dir_name:
            self.export_dir = dir_name
            self.export_dir_label.setText(f"OTIO Export Directory: {dir_name}")

    def select_output_dir(self):
        """Select the output directory."""
        dir_name = QFileDialog.getExistingDirectory(self, "Select Render Output Directory")
        if dir_name:
            self.output_dir = dir_name
            self.output_dir_label.setText(f"Render Output Directory: {dir_name}")

    def kitsu_edits(self):
        """Get the edits for the selected project."""
        try:
            import gazu

            project = self.project_map[self.projects_dropdown.currentText()]
            edits = gazu.edit.all_edits_for_project(project)

            
            
            if edits:
                self.edits_dropdown.clear()
                self.edits_dropdown.addItem("Select Kitsu Edit")
                for edit in edits:
                    name = edit["name"]
                    id = edit["id"]
                    self.edits_dropdown.addItem(name)

                print(f"Loaded {len(edits)} edits from Kitsu.")
            else:
                print("No edits found for the selected project.")
                self.edits_dropdown.clear()
                self.edits_dropdown.addItem("No Edits Found")
        except Exception as e:
            print(f"Failed to fetch Kitsu edits: {e}")
    

    def kitsu_edit_tasks(self):
        """Get the tasks for the selected edit."""
        try:
            import gazu
            
            project = self.project_map[self.projects_dropdown.currentText()]
            edit = str(self.edits_dropdown.currentText())
            edit_entity = gazu.edit.get_edit_by_name(project, edit)
            edit_id = edit_entity["id"]

            tasks = gazu.task.all_tasks_for_edit(edit_id)

            if tasks:
                self.edit_tasks_dropdown.clear()
                self.edit_tasks_dropdown.addItem("Select Kitsu Edit Task")
                for task in tasks:
                    name = task["task_type_name"]
                    task_id = task["id"]
                    self.edit_tasks_dropdown.addItem(name, task_id)

                print(f"Loaded {len(tasks)} tasks from Kitsu.")
            else:
                print("No tasks found for the selected edit.")
                self.edit_tasks_dropdown.clear()
                self.edit_tasks_dropdown.addItem("No Tasks Found")
        except Exception as e:
            print(f"Failed to fetch Kitsu tasks: {e}")

    def get_selections(self):
        """Get the user's selections as a dictionary."""

        self.selections = {
            "export_folder": self.export_dir,
            "output_folder": self.output_dir,
            "export_otio": self.export_otio_checkbox.isChecked(),
            "render_single_shots": self.single_shot_checkbox.isChecked(),
            "render_section_cut": self.section_cut_checkbox.isChecked(),
            "render_full_cut": self.full_cut_checkbox.isChecked(),
            "selected_render_preset": self.preset_dropdown.currentText(),
            "update_kitsu": self.upload_kitsu_checkbox.isChecked(),
            "selected_kitsu_project": self.projects_dropdown.currentText() if self.upload_kitsu_checkbox.isChecked() else None,
            "selected_kitsu_edit": self.edits_dropdown.currentText() if self.upload_kitsu_checkbox.isChecked() else None,
            #"selected_edit_task": self.edit_tasks_dropdown.currentText() if self.upload_kitsu_checkbox.isChecked() else None,  # Placeholder for task selection
            "selected_edit_task": self.get_selected_task_id() if self.upload_kitsu_checkbox.isChecked() else None,
            "description": self.comment.toPlainText()
        }
        return self.selections

    def on_project_selected(self, index):
        """Triggered when a project is selected from the dropdown."""
        if index > 0:  # Ignore the default "Select Kitsu Project" option
            selected_project_name = self.projects_dropdown.currentText()
            print(f"Selected project: {selected_project_name}")

            # Perform actions based on the selected project
            self.kitsu_edits()  # Example: Load edits for the selected project
        else:
            print("No project selected.")
            self.edits_dropdown.clear()
            self.edits_dropdown.addItem("Select Kitsu Edit")

    def on_edit_selected(self, index):
        """Triggered when an edit is selected from the dropdown."""
        if index > 0:  # Ignore the default "Select Kitsu Edit" option
            selected_edit_name = self.edits_dropdown.currentText()
            print(f"Selected edit: {selected_edit_name}")

            # Perform actions based on the selected edit
            self.kitsu_edit_tasks()
        else:
            print("No edit selected.")
            self.edit_tasks_dropdown.clear()
            self.edit_tasks_dropdown.addItem("Select Kitsu Edit Task")

    def get_selected_task_id(self):
        """Retrieve the ID of the selected task."""
        index = self.edit_tasks_dropdown.currentIndex()
        if index > 0:  # Ignore the default "Select Kitsu Edit Task" option
            task_id = self.edit_tasks_dropdown.itemData(index)  # Retrieve the stored task ID
            print(f"Selected task ID: {task_id}")
            return task_id
        else:
            print("No task selected.")
            return None       

    def cancel_and_exit(self):
        """Exit the GUI and terminate the process"""
        print("Operation cancelled by user.")
        self.close()
        os._exit(0)


    def start_process(self):
        """Retrieve selections and close the GUI"""
        if not self.export_dir or not self.output_dir:
            print("Please select both export and output directories.")
            return

        self.get_selections()

        selected_task_id = self.get_selected_task_id()

        self.close()


def run_gui(render_presets):
    """Function to run the GUI and return the user selections."""
    app = QApplication(sys.argv)
    window = ResolvePublisherGUI(render_presets)
    window.show()
    app.exec()

    # Return the selections as a dictionary after GUI closes
    return window.selections


if __name__ == "__main__":
    selections = run_gui()
    print("\nUser Selections:")
    for key, value in selections.items():
        print(f"{key}: {value}")
