import sevenbridges as sbg
from datetime import datetime, timedelta

# Authentication and Configuration
api = sbg.Api(url='https://cavatica-api.sbgenomics.com/v2', token='TOKEN_KEY')
project_id = 'yiran/variant-workbench-testing'

# Specify the date for which you want to get the list of failed tasks
specific_date = "2023-08-24"  # YYYY-MM-DD format
specific_datetime = datetime.strptime(specific_date, '%Y-%m-%d')

# Define the next day to use as the upper bound in our time range
next_day_datetime = specific_datetime + timedelta(days=1)

# Get all tasks within the project
all_tasks = api.tasks.query(project=project_id).all()

# Filter tasks by status and created time
failed_tasks = [
    task for task in all_tasks
    if task.status == 'FAILED'
    and specific_datetime <= task.created_time.replace(tzinfo=None) < next_day_datetime
]

# # Print the list of failed tasks
# for task in failed_tasks:
#     print(f"Task ID: {task.id}, Task name: {task.name}, Created at: {task.created_time}, Status: {task.status}")

# Print the list of failed tasks and the IDs of the input file 'vep_vcf'
for task in failed_tasks:
    # print(f"Task ID: {task.id}, Task name: {task.name}, Created at: {task.created_time}, Status: {task.status}")
    if 'vep_vcf' in task.inputs:
        vep_vcf_file = task.inputs['vep_vcf']
        # print(f"  Input vep_vcf ID: {vep_vcf_file.id}")
        print(vep_vcf_file.id)
    else:
        print("  Input vep_vcf not found.")