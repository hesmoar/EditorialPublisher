import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, 
    QCheckBox, QRadioButton, QButtonGroup, QFileDialog, QHBoxLayout
)
from PySide6.QtCore import Qt


class ResolvePublisherGUI(QMainWindow):
    """GUI for selecting export and render options"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editorial Publisher Settings")
        self.setGeometry(300, 200, 600, 400)

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Directory Selection
        self.export_dir_label = QLabel("OTIO export Directory: Not Selected")
        self.export_dir_button = QPushButton("Select OTIO export Directory")
        self.export_dir_button.clicked.connect(self.select_export_dir)

        self.output_dir_label = QLabel("Render Output Directory: Not Selected")
        self.output_dir_button = QPushButton("Select Render Output Directory")
        self.output_dir_button.clicked.connect(self.select_output_dir)

        layout.addWidget(self.export_dir_label)
        layout.addWidget(self.export_dir_button)
        layout.addWidget(self.output_dir_label)
        layout.addWidget(self.output_dir_button)

        # Render Options
        layout.addWidget(QLabel("Render Options:"))

        self.render_group = QButtonGroup()
        self.single_shot_radio = QRadioButton("Single Shots Only")
        self.section_cut_radio = QRadioButton("Section Render cut only")
        self.full_cut_radio = QRadioButton("Full Cut Only")
        self.all_radio = QRadioButton("All (Single + Section + Full Cut)")

        self.all_radio.setChecked(True)  # Default selection

        layout.addWidget(self.single_shot_radio)
        layout.addWidget(self.section_cut_radio)
        layout.addWidget(self.full_cut_radio)
        layout.addWidget(self.all_radio)

        self.render_group.addButton(self.single_shot_radio)
        self.render_group.addButton(self.section_cut_radio)
        self.render_group.addButton(self.full_cut_radio)
        self.render_group.addButton(self.all_radio)

        # Checkboxes
        self.export_otio_checkbox = QCheckBox("Export OTIO")
        self.upload_kitsu_checkbox = QCheckBox("Upload to Kitsu")

        layout.addWidget(self.export_otio_checkbox)
        layout.addWidget(self.upload_kitsu_checkbox)

        # Buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_process)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_and_exit)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.export_dir = ""
        self.output_dir = ""
        self.selections = {}

    # Select directory functions
    def select_export_dir(self):
        """Select the export directory."""
        dir_name = QFileDialog.getExistingDirectory(self, "Select OTIO Export Directory")
        if dir_name:
            self.export_dir = dir_name
            self.export_dir_label.setText(f"Export Directory: {dir_name}")

    def select_output_dir(self):
        """Select the output directory."""
        dir_name = QFileDialog.getExistingDirectory(self, "Select Render Output Directory")
        if dir_name:
            self.output_dir = dir_name
            self.output_dir_label.setText(f"Output Directory: {dir_name}")

    def get_selections(self):
        """Get the user's selections as a dictionary."""
        render_option = "both"
        if self.single_shot_radio.isChecked():
            render_option = "single"
        elif self.full_cut_radio.isChecked():
            render_option = "full"
        elif self.section_cut_radio.isChecked():
            render_option = "section"

        self.selections = {
            "export_folder": self.export_dir,
            "output_folder": self.output_dir,
            "export_otio": self.export_otio_checkbox.isChecked(),
            "render_single_shots": render_option == "single" or render_option == "both",
            "render_section_cut": render_option == "section" or render_option == "both",
            "render_full_cut": render_option == "full" or render_option == "both",
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


def run_gui():
    """Function to run the GUI and return the user selections."""
    app = QApplication(sys.argv)
    window = ResolvePublisherGUI()
    window.show()
    app.exec()

    # Return the selections as a dictionary after GUI closes
    return window.selections


if __name__ == "__main__":
    selections = run_gui()
    print("\nUser Selections:")
    for key, value in selections.items():
        print(f"{key}: {value}")
