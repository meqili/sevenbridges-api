import sevenbridges as sbg

# Authentication and Configuration
api = sbg.Api(url='https://cavatica-api.sbgenomics.com/v2', token='TOKEN_KEY')

# list all files under project
files = api.files.query(project='yiran/variant-workbench-testing').all()
for file in files:
    print(file.name)
# filter files by names
files = api.files.query(project='yiran/variant-workbench-testing').all()
# my_file = [file for file in files if 'chr8_exome_' in file.name]
my_file = [file for file in files if file.name.startswith('chr8_exome_') and 'vcf.gz' in file.name]
new_folder_path = '/virtual_human_exome_vcfs/chr8_exome' # New folder path
# Fetch the file object
# Move each file to the new folder
for file in my_file:
    file.move_to_folder(parent=new_folder_path)

# Task name
name = 'my-first-task'

# Project in which to run the task.
project = 'yiran/variant-workbench-testing'

# App to use to run the task
app = 'qqlii44/exonic-vcfs-post-process'


