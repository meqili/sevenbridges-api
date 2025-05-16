import sevenbridges as sbg
import argparse
import os

# Argument Parsing ------------
usage = """
Script: run_family_based_variant_filtering_app.py
Description: Submits tasks on Cavatica for family-based variant filtering.
Usage: python run_family_based_variant_filtering_app.py --run

Requirements:
- Environment variable SBG_API_TOKEN must be set
- All VCF and PED files must be in the same folder
- Files must follow naming conventions:
    - <fm_id>.ped
    - <anything>vep_105.vcf.gz
"""

parser = argparse.ArgumentParser(description='run app.', usage=usage)
parser.add_argument('--run', action='store_true', help='Include to run the task')
args = parser.parse_args()

# please change your inputs as needed ------------------
parent_folder = '66267dd276e36f4cdeeb6f8c'  # folder name for vcf files
family_hpo_file_id = '6671ad3ca193b42012ea8977' # input for wf
task_name_prefix = 'cranio_D3b_rerun' # name for task 

# Authentication and Configuration ------------------
TOKEN = os.environ.get("SBG_API_TOKEN")
if not TOKEN:
    raise ValueError("❌ SBG_API_TOKEN environment variable not set.")
api = sbg.Api(url="https://cavatica-api.sbgenomics.com/v2", token=TOKEN)

# Apps
project_id = 'yiran/variant-workbench-testing'  # Project in which to run the task.
app = 'yiran/variant-workbench-testing/family_based_variant_filtering_wf/'  # App to use to run the task

## existed tasks
# family_ids_file = open("family_ids.txt", "r") 
# task_family_ids = family_ids_file.read() 
# data_into_list = task_family_ids.split("\n") 

# put all vcf files in a same folder
all_files = list(api.files.query(parent=parent_folder).all())
for item in all_files:
    if item.name.endswith('vep_105.vcf.gz'):
        fm_id = item.metadata.get('Kids First Family ID')
        # if fm_id in data_into_list: 
        #     print(f"{fm_id} is already in the task list")
        #     continue       
        
        # Find matching ped file
        ped_matching_file = [file for file in all_files if file.name == f"{fm_id}.ped"]
        # hpo_matching_file = [file for file in items_in_parent_folder.all() if file.name == f"{fm_id}.HPO"]
        
        if not ped_matching_file:
            print(f"No matching ped file found for {fm_id}")
            continue
        if len(ped_matching_file) > 1:
            print(f"Multiple ped files found for {fm_id}")
            continue
        
        # Running app
        inputs = {
            'vep_vcf': api.files.get(item.id),
            'ped': api.files.get(ped_matching_file[0].id),
            # 'family_hpo_file': api.files.get(hpo_matching_file[0].id),
            'family_hpo_file': api.files.get(family_hpo_file_id),
            'fm_id': fm_id
        }

        # Task Configuration
        name = f'Family based variant filtering workflow (SNV/indel) run - {task_name_prefix} {fm_id}' #task name

        # Task Creation and Running
        run_status = args.run
        try:
            task = api.tasks.create(
                name=name, project=project_id, app=app, inputs=inputs, run=run_status
            )
            print(f'Task has been successfully created and ready to run for {fm_id}.')
        except sbg.SbgError as e:
            print(f'I was unable to run a task for {fm_id}. Error: {str(e)}')
