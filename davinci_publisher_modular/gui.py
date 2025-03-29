import sys
import os
import tkinter as tk
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QCheckBox, QRadioButton, QButtonGroup, QFileDialog, QHBoxLayout, QGroupBox, QFrame, QSpacerItem, QSizePolicy, QComboBox
)
from PySide6.QtCore import Qt
from render_utils import get_render_presets



list = ["Preset_1", "Preset_2", "Preset_3"]
#list = render_presets

class ResolvePublisherGUI(QMainWindow):
    """GUI for selecting export and render options"""

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
        self.single_shot_checkbox = QCheckBox("Single Shots Only")
        self.section_cut_checkbox = QCheckBox("Section Render cut only")
        self.full_cut_checkbox = QCheckBox("Full Cut Only")
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
        checkbox_layout = QVBoxLayout(checkbox_group)

        self.export_otio_checkbox = QCheckBox("Export OTIO")
        self.upload_kitsu_checkbox = QCheckBox("Upload to Kitsu")

        self.export_otio_checkbox.setChecked(True)
        self.upload_kitsu_checkbox.setChecked(True)

        checkbox_layout.addWidget(self.export_otio_checkbox)
        checkbox_layout.addWidget(self.upload_kitsu_checkbox)

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

        # Add some spacing
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        main_layout.addLayout(button_layout)

                # Store paths and selections
        #self.export_dir = ""
        #self.output_dir = ""
        #self.selections = {}

        # Apply stylesheet for a modern look
        self.apply_stylesheet()

    #def closeEvent(self, event):
    #    print("Operation cancelled by User")
    #    os._exit(0)
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
            "update_kitsu": self.upload_kitsu_checkbox.isChecked()
        }
        return self.selections

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
