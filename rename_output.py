import sevenbridges as sbg

# Authentication and Configuration
api = sbg.Api(url='https://cavatica-api.sbgenomics.com/v2', token='TOKEN_KEY')

# Task ID of the parent batch task
parent_task_id = '7a3d99ae-4272-46e3-aad3-e22318fa727a'
chromosome_interested = 'chr9'
project_id = '636e9c91c5da4f38ad474b39'   

# Get the parent task
parent_task = api.tasks.get(id=parent_task_id)

# Fetch the child tasks for the parent batch task
child_tasks = api.tasks.query(parent=parent_task_id).all()

# Iterate through the child tasks and print their outputs
# for child_task in child_tasks:
#     print(f"Child task ID: {child_task.id}")
#     for output_name, output_file in child_task.outputs.items():
#         # Assuming the output is a file, print the file ID
#         print(f"Output name: {output_name}, Output file ID: {output_file.id}")

output_files = []
for child_task in child_tasks:
    for output_name, output_file in child_task.outputs.items():
        # Assuming the output is a file, add it to the list
        output_files.append(output_file)

# Iterate through the output_files
for idx, output_file in enumerate(output_files):
    # Get the old folder ID
    old_folder_id = output_file.id
    # Define new folder name
    new_folder_name = f'_{idx}_{chromosome_interested}_exome_chunk_output_vcf' if idx != 0 else 'chr9_exome_chunk_output_vcf'
    # Create the new folder
    new_folder = api.files.create_folder(name=new_folder_name, parent=project_id)
    # Define the destination name for the copied file
    destination_name = output_file.name  # You can modify this if needed
    # Copy the file to the new folder (within the same project)
    new_file = output_file.copy(project=project_id, name=destination_name)
    print(f"File {output_file.name} has been copied to new folder {new_folder_name}")
    break