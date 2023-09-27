import sevenbridges as sbg
import argparse

# Argument Parsing ------------
usage = '''
Run a batch task on Cavatica.
Example:
    python AutoPVS1_rerun_batch_task.py --chromosome chr12 --run
'''
parser = argparse.ArgumentParser(description='Set chromosome of interest.', usage=usage)
parser.add_argument('--chromosome', required=True, help='Chromosome name (e.g., chr12)')
parser.add_argument('--run', action='store_true', help='Include to run the task')
args = parser.parse_args()
chromosome_interested = args.chromosome
print(f'Chromosome of interest: {chromosome_interested}')

# Authentication and Configuration ------------------
api = sbg.Api(url='https://cavatica-api.sbgenomics.com/v2', token='TOKEN_KEY')

# Task Configuration --------------------------------
# name = 'Kids First DRC Germline SNV Annotation Workflow run - ' + chromosome_interested  # Task name
project_id = 'yiran/variant-workbench-testing'           # Project in which to run the task.
app = 'yiran/variant-workbench-testing/kfdrc-autopvs1'  # App to use to run the task

# Setting Inputs -----------------------------------
# 1. files to run batch
parent_folder = '64b0140b7440d21289634fb4'
destination_folder_name = chromosome_interested
# Query all the files and folders in the given parent folder
items_in_parent_folder = api.files.query(parent=parent_folder)
# Filter for the folder by its name
destination_folder = next((item for item in items_in_parent_folder.all() if item.name == destination_folder_name and item.type == 'folder'), None)
# Query all files in the specified parent folder
all_files_in_folder = api.files.query(parent=destination_folder.id).all()
# Filter files that end with "vcf.gz"
exome_vep_vcf_files = [file for file in all_files_in_folder if file.name.endswith('.vcf.gz')]
# 2. other input
autopvs1_db_id = '6489d072ee36ac0be245bb0d'
autopvs1_db_file = api.files.get(id=autopvs1_db_id)

# Inputs
inputs = {}
inputs['vep_vcf'] = exome_vep_vcf_files
inputs['output_basename'] = chromosome_interested +  '_exome.vep_105.PAW'  # Add the output_basename input here
inputs['autopvs1_db'] = autopvs1_db_file

# Specify that one task should be created per file (i.e. batch tasks by file)
batch_by = {'type': 'item'}

# Specify that the batch input is 'vep_vcf'
batch_input = 'vep_vcf'  # Change this to match the app's input name


# Task Creation and Running -------------------------
run_status = args.run
name = 'AutoPVS1 RERUN - ' + chromosome_interested  # Task name
try:
    task = api.tasks.create(
        name=name, project=project_id, app=app, inputs=inputs,
        batch_input=batch_input, batch_by=batch_by, run=run_status
    )
    print('Batch task has been successfully created and run.')
except sbg.SbgError as e:
    print(f'I was unable to run a batch task. Error: {str(e)}')

# run_status = args.run
# for vcf_file in exome_vcf_files:
#     inputs['vep_vcf'] = vcf_file
#     name = 'Kids First DRC Germline SNV Annotation Workflow run - ' + vcf_file.name  # Task name
#     try:
#         task = api.tasks.create(
#             name=name, project=project_id, app=app, inputs=inputs, run=run_status
#         )
#         print(f'Task has been successfully created and run for {vcf_file.name}.')
#     except sbg.SbgError as e:
#         print(f'I was unable to run a task for {vcf_file.name}. Error: {str(e)}')
#     break
