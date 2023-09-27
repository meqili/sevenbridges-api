import sevenbridges as sbg
import argparse

# Authentication and Configuration ------------------
api = sbg.Api(url='https://cavatica-api.sbgenomics.com/v2', token='TOKEN_KEY')

# Task Configuration --------------------------------
# name = 'Kids First DRC Germline SNV Annotation Workflow run - ' + chromosome_interested  # Task name
project_id = 'd3b-bixu/sd-s9agk8xv-delivery'           # Project in which to run the task.
# app = 'yiran/variant-workbench-testing/kfdrc-germline-annot-vcf-filtering-wf/0'  # App to use to run the task

# Setting Inputs -----------------------------------
# 1. files to run batch
folder_id = '649343a7e669c06230ccb9e5'

# Get the folder object
folder = api.folders.get(id=folder_id, project=project_id)

# Query the files within that folder
files = api.files.query(project=project_id, folder=folder.id)

# Filter the files by Case ID metadata (replace 'metadata' and 'Case ID' with the appropriate fields)
filtered_files = [f for f in files.all() if f.metadata.get('Case ID') == 'Q1347']

# Print or collect the file IDs
file_ids = [f.id for f in filtered_files]
print(file_ids)