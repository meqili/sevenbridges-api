import sevenbridges as sbg
from datetime import datetime, timedelta

# Authentication and Configuration
api = sbg.Api(url='https://cavatica-api.sbgenomics.com/v2', token='TOKEN_KEY')
project_id = 'yiran/variant-workbench-testing'

# Define a function to retrieve tasks with a specific name pattern
def get_tasks_with_name_pattern(api, project_id, name_pattern):
    tasks = api.tasks.query(project=project_id).all()
    filtered_tasks = [task for task in tasks if name_pattern in task.name]
    return filtered_tasks

# Define a function to retrieve task id, name, and cost
def get_task_info(task):
    task_id = task.id
    task_name = task.name
    task_cost = task.price.amount if task.price else None  # Check if cost information is available
    return task_id, task_name, task_cost

# Filter tasks by name pattern and retrieve task info
name_pattern = "exonic_vcfs_post_process run"
filtered_tasks = get_tasks_with_name_pattern(api, project_id, name_pattern)

# Extract and print task id, name, and cost
for task in filtered_tasks:
    task_id, task_name, task_cost = get_task_info(task)
    print(f"Task ID: {task_id}, Task Name: {task_name}, Task Cost: {task_cost}")