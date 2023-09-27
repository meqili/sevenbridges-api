import sevenbridges as sbg
import argparse

# Argument Parsing ------------
usage = '''
Run a batch task on Cavatica.
Example:
    python exonic_vcfs_post_process_batch_task.py --chromosome chr12 --run
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
name = 'exonic_vcfs_post_process run - ' + chromosome_interested  # Task name
project_id = 'yiran/variant-workbench-testing'           # Project in which to run the task.
app = 'yiran/variant-workbench-testing/exonic-vcfs-post-process'  # App to use to run the task

# Setting Inputs -----------------------------------
# 1. files to run batch
# Read the folder IDs from the file
folder_ids = []
### sb files list --project yiran/variant-workbench-testing | grep chrY_exome_chunk_output_vcf
with open('chrY_exome_chunk_output_dir.list', 'r') as file:
    for line in file:
        folder_id = line.split('\t')[0].strip("'")
        folder_ids.append(folder_id)

# Inputs
inputs = {'input_vcf_dir': folder_ids}  # Note: Set it to the entire list of folder_ids

# Specify that one task should be created per file (i.e. batch tasks by file)
batch_by = {'type': 'item'}

# Specify that the batch input is 'input_vcf_dir'
batch_input = 'input_vcf_dir'  # Change this to match the app's input name

# Task Creation and Running -------------------------
run_status = args.run
try:
    task = api.tasks.create(
        name=name, project=project_id, app=app, inputs=inputs,
        batch_input=batch_input, batch_by=batch_by, run=run_status
    )
    print('Batch task has been successfully created and run.')
except sbg.SbgError as e:
    print(f'I was unable to run a batch task. Error: {str(e)}')


# for folder_id in folder_ids:
#     # Inputs for individual folder_id
#     inputs = {'input_vcf_dir': folder_id}

#     try:
#         task = api.tasks.create(
#             name=name, project=project_id, app=app, inputs=inputs,
#             run=run_status
#         )
#         print(f'Task for folder {folder_id} has been successfully created and run.')
#     except sbg.SbgError as e:
#         print(f'I was unable to run a task for folder {folder_id}. Error: {str(e)}')

