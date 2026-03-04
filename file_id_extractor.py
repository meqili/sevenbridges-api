import sevenbridges as sbg
import pandas as pd
import os

# Authentication and Configuration ------------------
TOKEN = os.environ.get("SBG_API_TOKEN")
if not TOKEN:
    raise ValueError("❌ SBG_API_TOKEN environment variable not set.")
api = sbg.Api(url="https://cavatica-api.sbgenomics.com/v2", token=TOKEN)

project_id = 'yiran/variant-workbench-testing'     
# Destination folder
parent_folder = '65dce70b1f31d93a416592eb' # folder name Q1777_germline

# Get all files in the parent folder
items_in_parent_folder = api.files.query(parent=parent_folder)

file_id_list = []
for item in items_in_parent_folder.all():
    new_file_id = {**{'File_Name': item.name}, **{'File_ID': item.id}, **item.metadata}
    file_id_list.append(new_file_id)

file_id_df = pd.DataFrame(file_id_list)


filtered_rows = file_id_df[file_id_df['File_Name'].str.contains("filtered3.bed")]
# Print the commands
for _, row in filtered_rows.iterrows():
    print(f"sudo sb download --file {row['File_ID']}")