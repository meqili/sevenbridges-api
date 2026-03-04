import sevenbridges as sbg
import argparse
import os

# Argument Parsing ------------
usage = '''
Run a batch task on Cavatica.
Example:
    python run_single_sample_variant_filtering_app.py --run
'''
parser = argparse.ArgumentParser(description='Set chromosome of interest.', usage=usage)
parser.add_argument('--run', action='store_true', help='Include to run the task')
args = parser.parse_args()

# Authentication and Configuration ------------------
TOKEN = os.environ.get("SBG_API_TOKEN")
if not TOKEN:
    raise ValueError("❌ SBG_API_TOKEN environment variable not set.")
api = sbg.Api(url="https://cavatica-api.sbgenomics.com/v2", token=TOKEN)

# Get the list of vcf file to run 
parent_folder = '696912c1bbaaa05f96c66984' 
items_in_parent_folder = api.files.query(parent=parent_folder)

## existed tasks
bs_ids_file = open("kids_first_biospecimen_id.list", "r") 
task_bs_ids = bs_ids_file.read() 
data_into_list = task_bs_ids.split("\n")

for item in items_in_parent_folder.all():
    if item.metadata.get('Kids First Biospecimen ID') in data_into_list:
        my_file = api.files.get(item.id)
        # Get existing tags (or initialize empty list)
        current_tags = my_file.tags or []
        if 'musculoskeletal_defect' not in current_tags:
            current_tags.append('musculoskeletal_defect')
            my_file.tags = current_tags
            my_file.save()
