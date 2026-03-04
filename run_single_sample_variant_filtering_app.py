import sevenbridges as sbg
import argparse
import os

# Argument Parsing ------------
usage = '''
Run a batch task on Cavatica.
Example:
    python run_single_sample_variant_filtering_app.py --run
'''
parser = argparse.ArgumentParser(description='Set chromosome of interest.', usage=usage)
parser.add_argument('--run', action='store_true', help='Include to run the task')
args = parser.parse_args()

# Authentication and Configuration ------------------
TOKEN = os.environ.get("SBG_API_TOKEN")
if not TOKEN:
    raise ValueError("❌ SBG_API_TOKEN environment variable not set.")
api = sbg.Api(url="https://cavatica-api.sbgenomics.com/v2", token=TOKEN)

# Apps
project_id = 'yiran/variant-workbench-testing'  # Project in which to run the task.
app = 'yiran/variant-workbench-testing/single-sample-VEP-variant-filtering-dragon-gene-group-wf'  # App to use to run the task

# Get the list of vcf file to run 
parent_folder = '696912c1bbaaa05f96c66984' 
items_in_parent_folder = api.files.query(parent=parent_folder)

## existed tasks
bs_ids_file = open("kids_first_biospecimen_id.list", "r") 
task_bs_ids = bs_ids_file.read() 
data_into_list = task_bs_ids.split("\n")

vcf_list = [
    item for item in items_in_parent_folder.all()
    if item.name.endswith('.vcf.gz') and item.metadata.get('Kids First Biospecimen ID') not in data_into_list
]

if not vcf_list:
    raise ValueError("❌ No matching VCF files found.")

chunk_size = 800

for i in range(0, len(vcf_list), chunk_size):
    vcf_list_chunk = vcf_list[i:i + chunk_size]
    # Inputs
    inputs = {
        'vep_vcf': vcf_list_chunk,   # <-- list of file objects
        'clinvar': True,
        'dbsnp': True,
        'genes': True
    }

    # Batch configuration
    batch_by = {'type': 'item'}
    batch_input = 'vep_vcf'

    task = api.tasks.create(
        name = f"Proband Only Batch {i}: Single Sample Variant Filtering",
        project=project_id,
        app=app,
        inputs=inputs,
        batch_input=batch_input,
        batch_by=batch_by,
        run=args.run
    )

    print(f"✅ Batch task created with {len(vcf_list_chunk)} subtasks.")