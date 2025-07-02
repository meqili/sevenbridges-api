import time
import sevenbridges as sbg
from sevenbridges.errors import TooManyRequests
import os

# Authentication and Configuration ------------------
TOKEN = os.environ.get("SBG_API_TOKEN")
if not TOKEN:
    raise ValueError("❌ SBG_API_TOKEN environment variable not set.")

api = sbg.Api(url="https://cavatica-api.sbgenomics.com/v2", token=TOKEN)

## settings
# Define the task name prefix to filter tasks
task_name_prefix = "single sample variant filtering workflow (VEP inputs) run - CBTN proband"
# Define the destination folder ID
destination_folder_id = '6862a3ae7baf5a5af9d9612f'

# Define the project ID
project_id = 'yiran/variant-workbench-testing'

# ------------------ Helper Functions ------------------
def api_call_with_retries(func, *args, **kwargs):
    try:
        result = func(*args, **kwargs)
        time.sleep(0.3)
        return result
    except TooManyRequests:
        print("🚨 Rate limit hit. Sleeping for 5 minutes before retrying...")
        time.sleep(310)  # 5 minutes and 10 seconds
        # Try once more after sleep
        return func(*args, **kwargs)

# Fetch the list of tasks under the specified project
tasks = api_call_with_retries(api.tasks.query, project=project_id).all()

# Filter tasks based on the specified name prefix
filtered_tasks = [task for task in tasks if task.name.startswith(task_name_prefix)]

# Helper function to move files and print details
def move_and_print(file_id):
    try:
        file = api_call_with_retries(api.files.get, id=file_id)
        print(f"Moving file: {file.name} (ID: {file.id})")
        moved_file = api_call_with_retries(file.move_to_folder, parent=destination_folder_id, name=file.name)
    except sbg.errors.NotFound:
        print(f"File with ID {file_id} does not exist and will be skipped.")

# Process each filtered task
for task in filtered_tasks:
    print(f"Processing Task ID: {task.id}, Task Name: {task.name}")
    
    # Fetch task details
    task_details = api_call_with_retries(api.tasks.get, id=task.id)

    # If it's a batch task, process its children
    if task_details.batch:
        print(f"Task {task.id} is a batch task. Fetching child tasks...")
        batch_children = api_call_with_retries(task_details.get_batch_children)

        for child in batch_children:
            print(f"Processing child task ID: {child.id}")
            child_details = api_call_with_retries(api.tasks.get, id=child.id)
            outputs = child_details.outputs
            if not outputs:
                print(f"No outputs for child task {child.id}")
                continue
            for output_name, file_info in outputs.items():
                if isinstance(file_info, list):
                    for file in file_info:
                        move_and_print(file.id)
                else:
                    move_and_print(file_info.id)
    else:
        # Non-batch task
        outputs = task_details.outputs
        if not outputs:
            print(f"No outputs for Task ID: {task.id}")
            continue
        for output_name, file_info in outputs.items():
            if isinstance(file_info, list):
                for file in file_info:
                    move_and_print(file.id)
            else:
                move_and_print(file_info.id)


print("All files have been processed and moved.")