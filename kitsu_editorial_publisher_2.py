import sys
import os
import subprocess

sys.path.append(r"D:\HecberryStuff\Dev\BetweenStudiosTools\Editorial_Publisher")

import davinci_publisher_standalone as drp

def run_external_script():
    # Path to the virtual environment's Python interpreter
    venv_python = r"D:\HecberryStuff\Dev\virtualEnv\Python313\Scripts\python.exe"
    # Path to the external script
    external_script_path = r"D:\HecberryStuff\Dev\BetweenStudiosTools\Editorial_Publisher\kitsu_editorial_publisher.py"
    

    
    # Run the external script using the virtual environment's Python interpreter
    subprocess.run([venv_python, external_script_path], check=True)

if __name__ == "__main__":
    # Your existing code to run inside Resolve
    # ...
    drp.delete_existing_jobs()
    edl_file_path = drp.export_edl()
    drp.render_jobs()
    
    print("Script 1 is done running now running script 2 in venv...")
    # Trigger the external script
    run_external_script()