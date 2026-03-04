import sevenbridges as sbg
import argparse
import pandas as pd
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

## check family ids and pt ids
file_path = "fm_pt_ids_crosswalk.csv"
df = pd.read_csv(file_path)

# Retrieve and print metadata for each file
for item in items_in_parent_folder.all():
    if item.name.endswith('vep_111.vcf.gz'):
        pt_id = item.metadata.get('Kids First Participant ID')
        fm_id = item.metadata.get('Kids First Family ID')

        if pt_id in df.kf_id.values:
            print(f'{pt_id} is found.')
        elif fm_id in df.family_id.values:
            print(f'{pt_id} is not found but {fm_id} found.')
        else:
            print(f'{pt_id} is not found.')
