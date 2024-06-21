import sevenbridges as sbg
import argparse

# Argument Parsing ------------
usage = '''
Run a batch task on Cavatica.
Example:
    python run_family_based_variant_filtering_app.py --run
'''
parser = argparse.ArgumentParser(description='Set chromosome of interest.', usage=usage)
parser.add_argument('--run', action='store_true', help='Include to run the task')
args = parser.parse_args()

# Authentication and Configuration ------------------
api = sbg.Api(url='https://cavatica-api.sbgenomics.com/v2', token='d188ed5269a1472d964311a2bb437f42')

# Get the list of vcf file to run 
parent_folder = '66267dd276e36f4cdeeb6f8c'  # folder name Cranio_D3b
items_in_parent_folder = api.files.query(parent=parent_folder)

# Apps
project_id = 'yiran/variant-workbench-testing'  # Project in which to run the task.
app = 'yiran/variant-workbench-testing/family_based_variant_filtering_wf/9'  # App to use to run the task

# Retrieve and print metadata for each file
for item in items_in_parent_folder.all():
    if item.name.endswith('vcf.gz'):
        fm_id = item.metadata.get('Kids First Family ID')
        
        # Find matching ped file
        ped_matching_file = [file for file in items_in_parent_folder.all() if file.name == f"{fm_id}.ped"]
        
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
            'family_hpo_file': api.files.get('6671ad3ca193b42012ea8977'),
            'fm_id': fm_id
        }

        # Task Configuration
        name = f'Family based variant filtering workflow (SNV/indel) run - {fm_id}'  # Task name

        # Task Creation and Running
        run_status = args.run
        try:
            task = api.tasks.create(
                name=name, project=project_id, app=app, inputs=inputs, run=run_status
            )
            print(f'Task has been successfully created and ready to run for {fm_id}.')
        except sbg.SbgError as e:
            print(f'I was unable to run a task for {fm_id}. Error: {str(e)}')
