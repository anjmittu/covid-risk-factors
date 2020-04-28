import pandas as pd
import os
import json
import glob
from data.data_utils import process_file

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

directories = [
        "comm_use_subset"
        # "biorxiv_medrxiv",
        # "noncomm_use_subset",
        # "custom_license"
    ]

corona_features = {"text": [None], "title": [None], "authors": [None], "authors_institutions": [None],
                   "abstract": [None], "paper_id": {None}}
corona_df = pd.DataFrame.from_dict(corona_features)

for directory in directories:
    print("Getting filenames for {}".format(directory))
    json_filenames = glob.glob(os.path.join(PROJECT_ROOT, "data/cord-19/{}/**/*.json".format(directory)), recursive=True)
    print("Loading papers to dataframe")
    for file_name in json_filenames[:10000]:
        with open(file_name) as json_data:
            data = json.load(json_data)
        clean_file = process_file(data)
        corona_df = corona_df.append(clean_file, ignore_index=True)

# Drop articles missing the text
corona_df = corona_df.dropna(subset=['text'])

if not os.path.exists(os.path.join(PROJECT_ROOT, "data/baseline")):
    os.makedirs(os.path.join(PROJECT_ROOT, "data/baseline"))

corona_df[['paper_id','text']].to_csv(os.path.join(PROJECT_ROOT, "data/baseline/papers.csv"), sep=" ", header=False, index=False)

