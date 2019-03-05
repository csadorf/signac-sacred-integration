from signac import init_project

project = init_project('signac-sacred-integration-minimal-example-project')

for i in range(10):
    project.open_job(dict(foo=i)).init()
