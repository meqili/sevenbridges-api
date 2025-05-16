"""
Script: move_outputs_from_tasks.py
Description: 
  - Queries completed tasks in a Cavatica project.
  - Filters by task name prefix.
  - Collects output files and moves them to a specified folder.

Requirements:
  - Environment variable SBG_API_TOKEN must be set.
  - destination_folder ID must be provided or defined.
"""
import sevenbridges as sbg
import json
from time import sleep
# from datetime import datetime
import requests
import os

# please change your inputs as needed ------------------
name_pattern = "Family based variant filtering workflow (SNV/indel) run - cranio_BDB_rerun" # task name filter
destination_folder = "682793907baf5a5af9cd2289"

# Authentication and Configuration ------------------
TOKEN = os.environ.get("SBG_API_TOKEN")
if not TOKEN:
    raise ValueError("❌ SBG_API_TOKEN environment variable not set.")
api = sbg.Api(url="https://cavatica-api.sbgenomics.com/v2", token=TOKEN)

# Output structure
output_json = {
    "items": []
}

# Get all tasks in the project
project_id = 'yiran/variant-workbench-testing'
# Define a function to retrieve tasks with a specific name pattern
def get_tasks_with_name_pattern(api, project_id, name_pattern):
    tasks = api.tasks.query(project=project_id).all()
    filtered_tasks = [task for task in tasks if name_pattern in task.name]
    return filtered_tasks

# Filter tasks by name pattern and retrieve task info
filtered_tasks = get_tasks_with_name_pattern(api, project_id, name_pattern)

# Filter and extract files from completed tasks on 2025-05-15
for task in filtered_tasks:
    if not task.end_time:
        continue  # skip if task hasn't finished

    # if task.end_time.date() == datetime(2025, 5, 15).date():
    for output_key, output_files in task.outputs.items():
        for file_obj in output_files:
            output_json["items"].append({
                "file": file_obj.id,
                "parent": destination_folder,  # ID of the *destination folder*
                "name": ""
            })

# Save or print the JSON
json_output = json.dumps(output_json, indent=2)
print(json_output)

# Optional: Save to a file
# with open("output_files.json", "w") as f:
#     f.write(json_output)

# move
API_URL = "https://cavatica-api.sbgenomics.com/v2/async/files/move"
HEADERS = {
    "Content-Type": "application/json",
    "X-SBG-Auth-Token": TOKEN
}

def move_files_in_batches(file_items, batch_size=20):
    for i in range(0, len(file_items), batch_size):
        batch = file_items[i:i + batch_size]
        payload = {"items": batch}
        
        response = requests.post(API_URL, headers=HEADERS, json=payload)

        if response.status_code == 202:
            print(f"✅ Batch {i//batch_size + 1} accepted: {response.json().get('id')}")
        else:
            print(f"❌ Batch {i//batch_size + 1} failed with status {response.status_code}:")
            print(response.text)

        sleep(2)  # Respectful pause between batches

# Assuming you already have output_json["items"]
move_files_in_batches(output_json["items"], batch_size=20)