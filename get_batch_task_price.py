import sevenbridges as sbg
import os
import csv

TOKEN = os.environ.get("SBG_API_TOKEN")
api = sbg.Api(
    url="https://cavatica-api.sbgenomics.com/v2",
    token=TOKEN
)

batch_id = "76bd4dcd-3519-4bf8-923a-f4e36e731339"

rows = []

for task in api.tasks.query(parent=batch_id).all():

    # 1️⃣ Get the vep_vcf input
    vep_input = task.inputs.get("vep_vcf")

    if not vep_input:
        continue

    # 2️⃣ Extract file ID
    # Usually format: {'class': 'File', 'path': 'project/file-id'}
    file_id = vep_input.get("id") or vep_input.get("path")

    if not file_id:
        continue

    # 3️⃣ Fetch file object
    file_obj = api.files.get(file_id)

    # 4️⃣ Get size (bytes)
    size_bytes = file_obj.size

    rows.append({
        "task_id": task.id,
        "vep_vcf_file": file_obj.name,
        "file_size_bytes": size_bytes,
        "price_usd": task.price.amount if task.price else None
    })

# Save to CSV
with open("subtask_vep_sizes.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["task_id", "vep_vcf_file", "file_size_bytes", "price_usd"]
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"Saved {len(rows)} rows.")