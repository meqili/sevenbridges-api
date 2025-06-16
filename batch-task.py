import sevenbridges as sbg
import os

# Authentication and Configuration ------------------
TOKEN = os.environ.get("SBG_API_TOKEN")
if not TOKEN:
    raise ValueError("❌ SBG_API_TOKEN environment variable not set.")
api = sbg.Api(url="https://cavatica-api.sbgenomics.com/v2", token=TOKEN)

##  assign the chromosome
import argparse
parser = argparse.ArgumentParser(description='Set chromosome of interest.')
parser.add_argument('--chromosome', required=True, help='Chromosome name (e.g., chr12)')
parser.add_argument('--run', action='store_true', help='Include to run the task')
args = parser.parse_args()
chromosome_interested = args.chromosome
print(f'Chromosome of interest: {chromosome_interested}')

# initiating ----------
name = 'get_exonic_vcfs run - ' + chromosome_interested # Task name
# Project in which to run the task.
project_id = 'yiran/variant-workbench-testing'
# App to use to run the task
app = 'yiran/variant-workbench-testing/get-exonic-vcfs'

# Setting Inputs ----------------
# 1. files to run batch
coord_files_id = '648cb913e669c06230cac2e6'
coord_folder_name = chromosome_interested + '.exonic.coord.chunk'
# Query all the files and folders in the given parent folder
items_in_parent_folder = api.files.query(parent=coord_files_id)
# Filter for the folder by its name
coord_folder = next((item for item in items_in_parent_folder.all() if item.name == coord_folder_name and item.type == 'folder'), None)
chuck_folder = api.files.get(coord_folder.id)
files_in_folder = list(api.files.query(parent=chuck_folder.id).all())  # Convert the generator to a list

# 2. whole genome vcf file
folder_id = '64932f90e669c06230cc9264'
vcf_file_name = chromosome_interested + '.vcf.gz'
# Get the folder object
folder = api.files.get(id=folder_id)
# Query for the file by name within the folder
files = api.files.query(parent=folder, names=[vcf_file_name])
# Assuming the file name is unique within the folder, you can get the file object
vcf_file = files[0] if files else None
vcf_file_id = api.files.get(vcf_file.id)

# Inputs
inputs = {}
inputs['exonic_coord_file'] = files_in_folder
inputs['wg_vcf_file'] = vcf_file_id
inputs['output_basename'] = chromosome_interested +  '_exome_chunk_'  # Add the output_basename input here


# Specify that one task should be created per file (i.e. batch tasks by file)
batch_by = {'type': 'item'}

# Specify that the batch input is 'exonic_coord_file'
batch_input = 'exonic_coord_file'  # Change this to match the app's input name

run_status = args.run

try:
    task = api.tasks.create(
        name=name, project=project_id, app=app, inputs=inputs,
        batch_input=batch_input, batch_by=batch_by, run=run_status
    )
    print('Batch task has been successfully created and run.')
except sbg.SbgError as e:  # Corrected exception name
    print(f'I was unable to run a batch task. Error: {str(e)}')