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
parent_folder = '6969131b19d55415d059b452' 
items_in_parent_folder = api.files.query(parent=parent_folder)

# Apps
project_id = 'yiran/variant-workbench-testing'  # Project in which to run the task.
app = 'yiran/variant-workbench-testing/split-family-joint-vcf'  # App to use to run the task

## existed tasks
task_fm_ids = pd.read_csv("fm_ped_file.csv")

# Retrieve and print metadata for each file
for item in items_in_parent_folder.all():
    if item.name.endswith('vep_111.vcf.gz'):
        fm_id = item.metadata.get('Kids First Family ID')
        if fm_id in task_fm_ids["family_id"].tolist():
            bs_id = task_fm_ids.loc[task_fm_ids['family_id'] == fm_id, 'sample_id'].iloc[0]
            # Running app
            inputs = {
                'family_joint_vcf': api.files.get(item.id),
                'proband_id': bs_id,
                'family_id':fm_id
            }

            # Task Configuration
            name = f'split-family-joint-vcf run -  {fm_id}'  # Task name

            # Task Creation and Running
            run_status = args.run
            try:
                task = api.tasks.create(
                    name=name, project=project_id, app=app, inputs=inputs, run=run_status
                )
                print(f'Task has been successfully created and ready to run for {fm_id}.')
            except sbg.SbgError as e:
                print(f'I was unable to run a task for {fm_id}. Error: {str(e)}')
