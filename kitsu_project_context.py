import kitsu_auth
import gazu

def get_project():
    active_projects = gazu.project.all_open_projects()


    return active_projects


def select_project():
    """
    Prompts the user to select a project from a list of available projects.
    Retrieves a list of projects, displays their names, and asks the user to 
    select one by entering the corresponding number. The function handles 
    invalid inputs and ensures a valid selection is made.
    Returns:
        str: The name of the selected project.
    """
    projects_to_pick = get_project()
    project_names = [project.get("name") for project in projects_to_pick]


    print("Please select an active project from the list:")
    for idx, project in enumerate(project_names, start=1):
        print(f"{idx}. {project}")
    
    # Request the user's choice
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(project_names):
                return project_names[choice - 1]  # Return the selected option
            else:
                print("Invalid choice. Please select a valid number from the list.")
        except ValueError:
            print("Please enter a valid number.")


