import time
import sevenbridges as sbg
from sevenbridges.errors import TooManyRequests
import os
import sys

# ------------------ Configuration ------------------
TOKEN = os.environ.get("SBG_API_TOKEN")
if not TOKEN:
    raise ValueError("❌ SBG_API_TOKEN environment variable not set.")

if len(sys.argv) != 3:
    print("Usage: python move_task_outputs_to_folder.py <TASK_ID> <DEST_FOLDER_ID>")
    sys.exit(1)

task_id = sys.argv[1]
destination_folder_id = sys.argv[2]

api = sbg.Api(url="https://cavatica-api.sbgenomics.com/v2", token=TOKEN)

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

def move_and_print(file_id):
    try:
        file = api_call_with_retries(api.files.get, id=file_id)
        print(f"Moving file: {file.name} (ID: {file.id}), current folder: {file.parent}")
        try:
            moved_file = api_call_with_retries(file.move_to_folder, parent=destination_folder_id, name=file.name)
            print(f"File moved to folder: {moved_file.parent}")
        except sbg.errors.Forbidden as e:
            print(f"Permission denied moving file {file.id}: {e}")
        except Exception as e:
            print(f"Other error moving file {file.id}: {e}")
    except sbg.errors.NotFound:
        print(f"File with ID {file_id} does not exist and will be skipped.")


# ------------------ Main Task Processing ------------------

print(f"Processing Task ID: {task_id}")
task_details = api_call_with_retries(api.tasks.get, id=task_id)

# Check for batch task
if task_details.batch:
    print(f"Task {task_id} is a batch task. Fetching child tasks...")
    batch_children = api_call_with_retries(task_details.get_batch_children, limit=100).all()

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
                    if file is not None:
                        move_and_print(file.id)
                    else:
                        print(f"⚠️ Skipping None output in list for output '{output_name}' in task {child.id}")
            elif file_info is not None:
                move_and_print(file_info.id)
            else:
                print(f"⚠️ Skipping None output '{output_name}' in task {child.id}")
else:
    outputs = task_details.outputs
    if not outputs:
        print(f"No outputs for Task ID: {task_id}")
    else:
        for output_name, file_info in outputs.items():
            if isinstance(file_info, list):
                for file in file_info:
                    move_and_print(file.id)
            else:
                move_and_print(file_info.id)

print("✅ All files have been processed and moved.")