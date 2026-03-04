import sevenbridges as sbg
import pandas as pd
import os

# Authentication and Configuration ------------------
TOKEN = os.environ.get("SBG_API_TOKEN")
if not TOKEN:
    raise ValueError("❌ SBG_API_TOKEN environment variable not set.")
api = sbg.Api(url="https://cavatica-api.sbgenomics.com/v2", token=TOKEN)

# Destination folder
parent_folder = '65d366fb1f31d93a415c1a2f' # folder name Q1777_germline

# Get all files in the parent folder
items_in_parent_folder = api.files.query(parent=parent_folder)

# Create an empty DataFrame
metadata_list = []

# Retrieve and print metadata for each file
for item in items_in_parent_folder.all():
    new_metadata = {**{'File_Name': item.name}, **{'File_ID': item.id}, **item.metadata}
    metadata_list.append(new_metadata)

# Display the DataFrame
metadata_df = pd.DataFrame(metadata_list)

# this family has three members
family_metadata_df = metadata_df[['Kids First Biospecimen ID', 'Kids First Participant ID', 'gender', 'Kids First Family ID', 'case_id']].drop_duplicates(keep='last')


# give gCNV file
filtered_rows = metadata_df[metadata_df['File_Name'].str.endswith("gatk_gcnv.genotyped_segments.vcf.gz") & 
                            (metadata_df['Kids First Biospecimen ID'] == 'BS_529GMFX4')]
# Print the filtered rows
print(filtered_rows)

# give gCNV file
filtered_rows = metadata_df[metadata_df['File_Name'].str.endswith(".cnvnator_call.vcf") & 
                            (metadata_df['Kids First Biospecimen ID'] == 'BS_529GMFX4')]
# Print the filtered rows
print(filtered_rows)