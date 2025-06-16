import sevenbridges as sbg
import argparse
import os

# Argument Parsing ------------
usage = '''
Run a batch task on Cavatica.
Example:
    python get_exonic_vcfs_batch_task.py --chromosome chr12 --run
'''
parser = argparse.ArgumentParser(description='Set chromosome of interest.', usage=usage)
parser.add_argument('--chromosome', required=True, help='Chromosome name (e.g., chr12)')
args = parser.parse_args()
chromosome_interested = args.chromosome
print(f'Chromosome of interest: {chromosome_interested}')

# Authentication and Configuration ------------------
TOKEN = os.environ.get("SBG_API_TOKEN")
if not TOKEN:
    raise ValueError("❌ SBG_API_TOKEN environment variable not set.")
api = sbg.Api(url="https://cavatica-api.sbgenomics.com/v2", token=TOKEN)

project_id = 'yiran/variant-workbench-testing'     
# Destination folder
parent_folder = '64b0140b7440d21289634fb4' # folder name virtual_human_exome_vcfs_vep_annotated
destination_folder_name = chromosome_interested
# Query all the files and folders in the given parent folder
items_in_parent_folder = api.files.query(parent=parent_folder)
# Filter for the folder by its name
destination_folder = next((item for item in items_in_parent_folder.all() if item.name == destination_folder_name and item.type == 'folder'), None)


# Check if destination_folder is None; if so, create it
if destination_folder is None:
    destination_folder = api.files.create_folder(name=destination_folder_name, parent=parent_folder)
    print(f"Folder '{destination_folder_name}' created.")
else:
    print(f"Folder '{destination_folder_name}' already exists.")