def get_current_project():

    resolve = app.GetResolve()
    projectManager = resolve.GetProjectManager()
    current_project = projectManager.GetCurrentProject()
    project = current_project.GetName()
    print(project)


    return current_project

get_current_project()