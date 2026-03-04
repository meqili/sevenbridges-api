import time
import sevenbridges as sbg
from sevenbridges.errors import TooManyRequests, NotFound, Forbidden
import os
import pandas as pd

# ------------------ Authentication ------------------
TOKEN = os.environ.get("SBG_API_TOKEN")
if not TOKEN:
    raise ValueError("❌ SBG_API_TOKEN environment variable not set.")

api = sbg.Api(url="https://cavatica-api.sbgenomics.com/v2", token=TOKEN)

# ------------------ Config ------------------
project_id = 'yiran/variant-workbench-testing'
parent_folder = '6862a3ae7baf5a5af9d9612f'
destination_folder = '68b875b72ec4323ac63550ad'

# ------------------ Helper: Retry Wrapper ------------------
def api_call_with_retries(func, *args, **kwargs):
    try:
        result = func(*args, **kwargs)
        time.sleep(0.3)  # light throttle
        return result
    except TooManyRequests:
        print("🚨 Rate limit hit. Sleeping for 5 minutes before retrying...")
        time.sleep(310)  # 5 minutes + buffer
        return func(*args, **kwargs)

# ------------------ Load participant IDs ------------------
q_ptps_df = pd.read_csv("/Users/liq3/PhD_project/analysis/ehr_code_to_hpo_mapping/q_case_ids.csv")
participant_ids = set(q_ptps_df["case_id"].tolist())

# ------------------ List and Process Files ------------------
files_in_parent = api_call_with_retries(
    api.files.query, parent=parent_folder
).all()

for f in files_in_parent:
    try:
        file_obj = api_call_with_retries(api.files.get, id=f.id)
        participant_id = file_obj.metadata.get("case_id")

        if participant_id in participant_ids:
            print(f"➡️ Moving {file_obj.name} (ID: {file_obj.id}) [Participant {participant_id}]")
            try:
                moved_file = api_call_with_retries(file_obj.move_to_folder, parent=destination_folder, name=file_obj.name)
                print(f"   ✅ Moved to folder {moved_file.parent}")
            except Forbidden as e:
                print(f"   ❌ Permission denied moving {file_obj.id}: {e}")
            except Exception as e:
                print(f"   ❌ Other error moving {file_obj.id}: {e}")
        else:
            print(f"⏭️ Skipped {file_obj.name} (ID: {file_obj.id}) – Participant {participant_id} not in list")

    except NotFound:
        print(f"⚠️ File {f.id} not found, skipping.")
    except Exception as e:
        print(f"⚠️ Unexpected error with file {f.id}: {e}")

print("🏁 Done processing all files.")
