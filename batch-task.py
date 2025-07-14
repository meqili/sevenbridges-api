import sevenbridges as sbg
import argparse
import os

# Argument Parsing ------------
parser = argparse.ArgumentParser()
parser.add_argument('--run', action='store_true', help='Include to run the task')
args = parser.parse_args()

# Authentication and Configuration ------------------
TOKEN = os.environ.get("SBG_API_TOKEN")
if not TOKEN:
    raise ValueError("❌ SBG_API_TOKEN environment variable not set.")
api = sbg.Api(url="https://cavatica-api.sbgenomics.com/v2", token=TOKEN)

# Task Configuration --------------------------------
# name = 'Kids First DRC Germline SNV Annotation Workflow run - ' + chromosome_interested  # Task name
project_id = 'kfdrc-harmonization/sd-bhjxbdqk-x01-germline-sv'           # Project in which to run the task.
app = 'kfdrc-harmonization/sd-bhjxbdqk-x01-germline-sv/structure-variant-filtering-wf'  # App to use to run the task

# Setting Inputs -----------------------------------
all_files = list(api.files.query(project=project_id, limit=100).all())
annotated_tsvs = [f for f in all_files if f.name.endswith('annotated.tsv')]
gene_list_file = api.files.get(id='68755548799cc519908c6b4a')

# Inputs
inputs = {}
inputs['annotated_sv_file'] = annotated_tsvs
inputs['gene_list_file'] = gene_list_file
inputs['field_separator'] = 'tab'
inputs['filter_gene_name'] = True
inputs['filter_re_gene'] = True

batch_by = {'type': 'item'}
batch_input = 'annotated_sv_file'  # Change this to match the app's input name


# Task Creation and Running -------------------------
run_status = args.run
name = 'Structure-Variant-Filtering-wf - CBTN part 2'  # Task name
try:
    task = api.tasks.create(
        name=name, project=project_id, app=app, inputs=inputs,
        batch_input=batch_input, batch_by=batch_by, run=run_status
    )
    print('Batch task has been successfully created and run.')
except sbg.SbgError as e:
    print(f'I was unable to run a batch task. Error: {str(e)}')
