import sys
import os
import pprint
import tkinter as tk
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QCheckBox, QRadioButton, QButtonGroup, QFileDialog, QHBoxLayout, QGroupBox, QFrame, QSpacerItem, QSizePolicy, QComboBox, QTextEdit
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from render_utils import get_render_presets
from kitsu_project_context import project_context, task_context, get_project




class ResolvePublisherGUI(QMainWindow):
    """GUI for selecting export and render options"""

    project_id, project_name = project_context()
    task_id, task_name = task_context()

    def on_kitsu_checkbox_changed(self, state):
        """Triggered when Upload to Kitsu checkbox is toggled."""
        if state == 2: # If checked
            try:
                import gazu
                from kitsu_auth import kitsu_auto_login


                print("Logging into Kitsu and fetching projects...")
                kitsu_auto_login()
                #project_id, project_name = project_context()

                #TODO: Remove unnecesary code 

                #self.projects_dropdown.clear()
                #self.projects_dropdown.addItem("Select Kitsu Project")
                #self.project_map = {}
#
                #for project in projects:
                #    name = project["name"]
                #    self.projects_dropdown.addItem(name)
                #    self.project_map[name] = project
                #
                #print(f"Loaded {len(projects)} projects from Kitsu.")
                print(f"Succesfuly loaded context project: {self.project_name}")

                self.kitsu_dropdown_group.setVisible(True)
            except Exception as e:
                print(f"Failed to fetch Kitsu projects: {e}")
                self.kitsu_dropdown_group.setVisible(False)
        else:

            #self.projects_dropdown.clear()
            #self.projects_dropdown.addItem("Kitsu not enabled")
            self.kitsu_dropdown_group.setVisible(False)


    def __init__(self, presets):
        super().__init__()
        self.setWindowTitle("Editorial Publisher Settings")
        icon_path = r"D:\HecberryStuff\Dev\BetweenStudiosTools\Editorial_Tools\TaskManager\icons\KitsuPublisherIcon.ico"
        self.setWindowIcon(QIcon(icon_path))
        self.setGeometry(300, 200, 650, 450)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Create a horizontal layout for two columns
        first_level_columns_layout = QHBoxLayout()

        # Left Column (Render and Export Options)
        left_column_layout = QVBoxLayout()

        # Render and Export Options
        render_group = QGroupBox("Render and Export Options")
        render_layout = QVBoxLayout(render_group)

        self.single_shot_checkbox = QCheckBox("Single Shots")
        self.section_cut_checkbox = QCheckBox("Section Render cut")
        self.full_cut_checkbox = QCheckBox("Full Cut")
        self.single_shot_checkbox.setChecked(True)  # Default selections
        self.full_cut_checkbox.setChecked(True)

        render_layout.addWidget(self.single_shot_checkbox)
        render_layout.addWidget(self.section_cut_checkbox)
        render_layout.addWidget(self.full_cut_checkbox)

        left_column_layout.addWidget(render_group)

        # Right Column (Checkbox or Export Options)
        right_column_layout = QVBoxLayout()

        # Export Options
        checkbox_group = QGroupBox("Export Options")
        checkbox_layout = QVBoxLayout(checkbox_group)

        self.export_otio_checkbox = QCheckBox("Export OTIO")
        self.upload_kitsu_checkbox = QCheckBox("Upload to Kitsu")
        self.upload_kitsu_checkbox.stateChanged.connect(self.on_kitsu_checkbox_changed)

        self.export_otio_checkbox.setChecked(True)
        self.upload_kitsu_checkbox.setChecked(False)

        checkbox_layout.addWidget(self.export_otio_checkbox)
        checkbox_layout.addWidget(self.upload_kitsu_checkbox)

        right_column_layout.addWidget(checkbox_group)

        # Add the two columns to the horizontal layout
        first_level_columns_layout.addLayout(left_column_layout)
        first_level_columns_layout.addLayout(right_column_layout)

        # Add the columns layout to the main layout
        main_layout.addLayout(first_level_columns_layout)

        # Second level columns layout
        second_level_columns_layout = QHBoxLayout()

        # Second level Left Column --
        second_left_column_layout = QVBoxLayout()

        # Kitsu Dropdown Section ---------------------------------------------------
        self.kitsu_dropdown_group = QGroupBox("Kitsu Context")
        kitsu_dropdown_layout = QVBoxLayout(self.kitsu_dropdown_group)

        #FIXME: This section should show the information of the context from Kitsu, we dont need the user input anymore.


        self.kitsu_project_label = QLabel(self.project_name)
        self.kitsu_task_label = QLabel(self.task_name)
        kitsu_dropdown_layout.addWidget(self.kitsu_project_label)
        kitsu_dropdown_layout.addWidget(self.kitsu_task_label)
        
        #self.projects_dropdown = QComboBox()
        #self.projects_dropdown.addItems(["Select Kitsu Project"])
        #self.projects_dropdown.currentIndexChanged.connect(self.on_project_selected)
        #kitsu_dropdown_layout.addWidget(QLabel("Select Kitsu Project:"))
        #kitsu_dropdown_layout.addWidget(self.projects_dropdown)

        #self.edits_dropdown = QComboBox()
        #self.edits_dropdown.addItems(["Select Kitsu Edit"])
        #self.edits_dropdown.currentIndexChanged.connect(self.on_edit_selected)
        #kitsu_dropdown_layout.addWidget(QLabel("Select Kitsu Edit:"))
        #kitsu_dropdown_layout.addWidget(self.edits_dropdown)

        #self.edit_tasks_dropdown = QComboBox()
        #self.edit_tasks_dropdown.addItems(["Select Kitsu Edit Task"])
        #kitsu_dropdown_layout.addWidget(QLabel("Select Kitsu Edit Task:"))
        #kitsu_dropdown_layout.addWidget(self.edit_tasks_dropdown)

        #self.shot_task_dropdown = QComboBox()
        #self.shot_task_dropdown.addItems(["Select Shot Task"])
        #self.shot_task_dropdown.currentIndexChanged.connect(self.on_shot_task_selected)
        #kitsu_dropdown_layout.addWidget(QLabel("Select Shot Task:"))
        #kitsu_dropdown_layout.addWidget(self.shot_task_dropdown)   


        self.kitsu_dropdown_group.setVisible(False)  # Initially hidden
        second_left_column_layout.addWidget(self.kitsu_dropdown_group)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        second_left_column_layout.addItem(spacer)


        # Second level Right Column --
        second_right_column_layout = QVBoxLayout()

        # Resolve Dropdown Section ---------------------------------------------------
        resolve_dropdown_group = QGroupBox("Resolve Settings selection")
        resolve_dropdown_layout = QVBoxLayout(resolve_dropdown_group)

        self.preset_dropdown = QComboBox()
        self.preset_dropdown.addItems(presets)
        resolve_dropdown_layout.addWidget(QLabel("Select Render Preset:"))
        resolve_dropdown_layout.addWidget(self.preset_dropdown) 


        # Adding resolve dropdown to the second right column layout
        resolve_dropdown_group.setVisible(True)  # Initially visible
        second_right_column_layout.addWidget(resolve_dropdown_group)



        # Adding the two second level columns to the horizontal layout
        second_level_columns_layout.addLayout(second_left_column_layout)
        second_level_columns_layout.addLayout(second_right_column_layout)


        # Add the second level columns layout to the main layout
        main_layout.addLayout(second_level_columns_layout)


        # Directory Selection -------------------------------------------------
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

        main_layout.addWidget(dir_group)

        # Comment Section ---------------------------------------------------
        comment_group = QGroupBox("Preview Comment")
        comment_layout = QVBoxLayout(comment_group)

        self.comment_label = QLabel("Add a description for the shot")
        self.comment = QTextEdit(self)

        comment_layout.addWidget(self.comment_label)
        comment_layout.addWidget(self.comment)

        main_layout.addWidget(comment_group)

        # Buttons ---------------------------------------------------
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_process)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_and_exit)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.cancel_button)

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

    def get_kitsu_shot_tasks(self):
        try:
            import gazu

            project = self.project_map[self.projects_dropdown.currentText()]
            project_tasks = gazu.task.all_task_types_for_project(project)
            #tasks_for_list = []
            #pprint.pprint(kitsu_entity_types)
            if project_tasks:
                self.shot_task_dropdown.clear()
                self.shot_task_dropdown.addItem("Select Shot Task")
                #tasks_for_list.append("Select Shot Task")
                for task in project_tasks:
                    if task.get("for_entity") == "Shot":
                        task_name = task.get("name")
                        self.shot_task_dropdown.addItem(task_name)
                        print(f"Loaded tasks for {task.get('for_entity')}")
            else:
                print("No tasks found for selected project entity: Shot")
                self.shot_task_dropdown.clear()
                self.shot_task_dropdown.addItem("No Tasks Found")

        except Exception as e:
            print(f"Failed to fetch Kitsu shot tasks: {e}")


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
            "selected_kitsu_project": self.project_name if self.upload_kitsu_checkbox.isChecked() else None,
            #"selected_kitsu_project": self.projects_dropdown.currentText() if self.upload_kitsu_checkbox.isChecked() else None,
            "selected_kitsu_edit": self.edits_dropdown.currentText() if self.upload_kitsu_checkbox.isChecked() else None,
            "selected_edit_task": self.get_selected_task_id() if self.upload_kitsu_checkbox.isChecked() else None,
            "selected_shot_task": self.shot_task_dropdown.currentText() if self.upload_kitsu_checkbox.isChecked() else None,
            "description": self.comment.toPlainText()
        }
        return self.selections

    def on_shot_task_selected(self, index):
        pass


    def on_project_selected(self, index):
        """Triggered when a project is selected from the dropdown."""
        if index > 0:  # Ignore the default "Select Kitsu Project" option
            selected_project_name = self.projects_dropdown.currentText()
            print(f"Selected project: {selected_project_name}")

            # Perform actions based on the selected project
            self.kitsu_edits()  # Example: Load edits for the selected project
            self.get_kitsu_shot_tasks()  # Example: Load tasks for the selected project
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
