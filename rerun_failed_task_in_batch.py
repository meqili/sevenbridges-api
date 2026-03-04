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

batch_id = "76bd4dcd-3519-4bf8-923a-f4e36e731339"

# Apps
project_id = 'yiran/variant-workbench-testing'  # Project in which to run the task.
app = 'yiran/variant-workbench-testing/single-sample-VEP-variant-filtering-dragon-gene-group-wf'  # App to use to run the task

# Get all subtasks
tasks = api.tasks.query(parent=batch_id).all()
failed_tasks = [t for t in tasks if t.status == "FAILED"]

# Collect vep_vcf files from all failed tasks
vcf_list = []

for task in failed_tasks:
    vep_input = task.inputs.get("vep_vcf")
    if vep_input:
        # vep_input is a dict like {'class': 'File', 'id': 'project/file-id'}
        file_id = vep_input.get("id") or vep_input.get("path")
        if file_id:
            # Wrap as an "item" for batch rerun
            vcf_list.append({
                "class": "File",
                "path": file_id
            })

# Prepare inputs for the batch rerun
inputs = {
    "vep_vcf": vcf_list,   # list of failed vep_vcf files
    "clinvar": True,
    "dbsnp": True,
    "genes": True
}

# Batch configuration
batch_by = {"type": "item"}
batch_input = "vep_vcf"

# Create batch task to rerun failed tasks
task = api.tasks.create(
    name=f"Proband Only Batch Rerun: Single Sample Variant Filtering",
    project=project_id,
    app=app,
    inputs=inputs,
    batch_input=batch_input,
    batch_by=batch_by,
    run=args.run
)

print(f"Batch rerun task created: {task.id}")