import sevenbridges as sbg
import argparse
import os

# Argument Parsing ------------
usage = '''
Run a batch task on Cavatica.
Example:
    python run_GBVF_spark35_task.py --run
'''
parser = argparse.ArgumentParser(description='Set chromosome of interest.', usage=usage)
parser.add_argument('--run', action='store_true', help='Include to run the task')
args = parser.parse_args()

# Authentication and Configuration ------------------
TOKEN = os.environ.get("SBG_API_TOKEN")
if not TOKEN:
    raise ValueError("❌ SBG_API_TOKEN environment variable not set.")
api = sbg.Api(url="https://cavatica-api.sbgenomics.com/v2", token=TOKEN)

# Get the list of gene list file to run 
parent_folder = '6803139e2b97f154cfea3102'
items_in_parent_folder = api.files.query(parent=parent_folder)


# Apps
project_id = 'yiran/variant-workbench-testing'  # Project in which to run the task.
app = 'yiran/variant-workbench-testing/gene-based-variant-filtering-wf-spark35'  # App to use to run the task

# Retrieve and print metadata for each file
for item in items_in_parent_folder.all():
        file_name = item.name
        # Running app
        inputs = {
            'gene_list': api.files.get(item.id),
            'occurrences': api.files.get('67ffc5d27baf5a5af9c70bc4'),
            'participant_list': api.files.get('6803139f2b97f154cfea3119'),
            'clinvar': api.files.get('6840557f2b97f154cfc153b9'),
            'consequences': True,  # App setting for Consequences
            'diagnoses': True,  # App setting for Diagnoses
            'output_basename': file_name, # App setting for output basename
            'phenotypes': True,  # App setting for Phenotypes
            'studies': True,  # App setting for Studies
            'variants': True,  # App setting for Variants
        }

        # Task Configuration
        name = f'Gene_Based_Variant_Filtering (spark 3.5 ver) {file_name}'  # Task name

        # Task Creation and Running
        run_status = args.run
        try:
            task = api.tasks.create(
                name=name, project=project_id, app=app, inputs=inputs, run=run_status,
                execution_settings={
                    "instance_type": "c4.2xlarge;ebs-gp2;2000",
                    "max_parallel_instances": 1
                }
            )
            print(f'Task has been successfully created and ready to run for {file_name}.')
        except sbg.SbgError as e:
            print(f'I was unable to run a task for {file_name}. Error: {str(e)}')
