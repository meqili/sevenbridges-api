import sevenbridges as sbg
import argparse

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
api = sbg.Api(url='https://cavatica-api.sbgenomics.com/v2', token='TOKEN_KEY')
project_id = 'yiran/variant-workbench-testing'     
# Destination folder
parent_folder = '64b0140b7440d21289634fb4' # folder name virtual_human_exome_vcfs_vep_annotated
destination_folder_name = chromosome_interested
# Query all the files and folders in the given parent folder
items_in_parent_folder = api.files.query(parent=parent_folder)
# Filter for the folder by its name
destination_folder = next((item for item in items_in_parent_folder.all() if item.name == destination_folder_name and item.type == 'folder'), None)

# Query all files in the project
all_files = api.files.query(project=project_id).all()

# Filter files based on pattern
files_to_move = [file for file in all_files if file.name.startswith(chromosome_interested + '_exome.vep') and (file.name.endswith('.vcf.gz') or file.name.endswith('.vcf.gz.tbi'))]

# Get the destination folder object
destination_folder_obj = api.files.get(id=destination_folder.id)

# Loop through files you want to move
for file in files_to_move:
    try:
        # Update the parent ID with the ID of the destination folder
        file = file.copy(project=destination_folder.id, name=file.name)
        print(f'Successfully moved {file.name} to {destination_folder_obj.name}')
    except Exception as e:
        print(f'Failed to move {file.name}. Error: {str(e)}')
