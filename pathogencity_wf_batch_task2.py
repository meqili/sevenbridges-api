import sevenbridges as sbg
import argparse
import re
import os

# Argument Parsing ------------
usage = '''
Run a batch task on Cavatica.
Example:
    python pathogencity_wf_batch_task2.py --run
'''
parser = argparse.ArgumentParser(description='Set chromosome of interest.', usage=usage)
parser.add_argument('--run', action='store_true', help='Include to run the task')
args = parser.parse_args()

# Authentication and Configuration ------------------
TOKEN = os.environ.get("SBG_API_TOKEN")
if not TOKEN:
    raise ValueError("❌ SBG_API_TOKEN environment variable not set.")
api = sbg.Api(url="https://cavatica-api.sbgenomics.com/v2", token=TOKEN)

# Task Configuration --------------------------------
# name = 'Kids First DRC Germline SNV Annotation Workflow run - ' + chromosome_interested  # Task name
project_id = 'yiran/variant-workbench-testing'           # Project in which to run the task.
app = 'yiran/variant-workbench-testing/pathogenicity-preprocessing-workflow2/4'  # App to use to run the task

# Setting Inputs -----------------------------------
# 1. files to run batch
# Query all the files under project
all_files_in_folder = api.files.query(project=project_id).all()
# Filter files that end with "vcf.gz"
exome_vep_vcf_files = [file for file in all_files_in_folder if file.name.endswith('_exome.vep_105.vcf.gz')]

for small_vep_file in exome_vep_vcf_files:
    chromosome_interested = re.search(r'chr\d+', small_vep_file.name).group()
    # print(chromosome_interested)
    # Inputs
    inputs = {}
    inputs['vep_vcf'] = small_vep_file
    inputs['output_basename'] = chromosome_interested +  '_exome.vep_105.PAW'  # Add the output_basename input here
    inputs['annovar_ram'] = 128
    inputs['bcftools_strip_info'] = '^INFO/CSQ'
    inputs['intervar_ram'] = 200

    # Task Creation and Running -------------------------
    run_status = args.run  # Assuming args.run holds the status whether to run the task immediately
    name = 'Pathogenicity Preprocessing Workflow run - ' + chromosome_interested  # Task name

    try:
        task = api.tasks.create(
            name=name, project=project_id, app=app, inputs=inputs, run=run_status
        )
        print('Single task has been successfully created and run.')
    except sbg.SbgError as e:
        print(f'I was unable to run a single task. Error: {str(e)}')