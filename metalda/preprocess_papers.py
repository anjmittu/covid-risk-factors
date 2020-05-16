import pandas as pd
import os
import json
import glob
from data.data_utils import process_file
import csv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

directories = [
    "comm_use_subset",
    "biorxiv_medrxiv",
    "noncomm_use_subset",
    "custom_license"
]

metadata_table = pd.read_csv(os.path.join(PROJECT_ROOT, "data/cord-19/metadata.csv"))
article_metadata = {row["sha"]: row for index, row in metadata_table.iterrows()}

corona_features = {"text": [None], "title": [None], "authors": [None], "authors_institutions": [None],
                   "abstract": [None], "paper_id": {None}, "pub_date_str": {None}, "disease_epoch": {None}}
corona_df = pd.DataFrame.from_dict(corona_features)

total_rejected_papers = 0

for directory in directories:
    print("Getting file names for {}".format(directory))
    json_filenames = glob.glob(os.path.join(PROJECT_ROOT, "data/cord-19/{}/**/*.json".format(directory)),
                               recursive=True)
    print("Loading papers to dataframe")
    for i, file_name in enumerate(json_filenames):
        if "pmc_json" not in file_name:
            with open(file_name) as json_data:
                data = json.load(json_data)
            clean_file = process_file(data, article_metadata)
            if len(clean_file) == 0:
                total_rejected_papers += 1
            if "paper_id" in clean_file and clean_file["paper_id"] == "7e643a4495a525bf9d9760636f6c13daf8216d2a":
                # removing due to non-english words
                clean_file = {}
                total_rejected_papers += 1
                print("removing paper")
            corona_df = corona_df.append(clean_file, ignore_index=True)
            if i % 1000 == 0:
                print("Papers processed: {}, num rejected: {}".format(i, total_rejected_papers))

print("removed {} papers".format(total_rejected_papers))

# Drop articles missing the text
corona_df = corona_df.dropna(subset=['text'])

if not os.path.exists(os.path.join(PROJECT_ROOT, "data/mallet/institution")):
    os.makedirs(os.path.join(PROJECT_ROOT, "data/mallet/institution"))

if not os.path.exists(os.path.join(PROJECT_ROOT, "data/mallet/epoch")):
    os.makedirs(os.path.join(PROJECT_ROOT, "data/mallet/epoch"))

# Drop articles missing the institution
corona_df_institution = corona_df.dropna(subset=['authors_institutions'])

corona_df_institution.to_csv(os.path.join(PROJECT_ROOT, "data/mallet/institution/papers.csv"),
                             sep="\t",
                             header=False,
                             index=False,
                             columns=["paper_id", "authors_institutions", "text"],
                             quoting=csv.QUOTE_NONE,
                             escapechar='\\')

# Drop articles missing the epoch
corona_df_epoch = corona_df.dropna(subset=['disease_epoch'])

corona_df_epoch.to_csv(os.path.join(PROJECT_ROOT, "data/mallet/epoch/papers.csv"),
                       sep="\t",
                       header=False,
                       index=False,
                       columns=["paper_id", "disease_epoch", "text"],
                       quoting=csv.QUOTE_NONE,
                       escapechar='\\')

# Drop articles missing the epoch and institution
corona_df_epoch_institution = corona_df.dropna(subset=['disease_epoch', "authors_institutions"])

corona_df_epoch_institution.to_csv(os.path.join(PROJECT_ROOT, "data/mallet/papers.csv"),
                                   sep="\t",
                                   header=False,
                                   index=False,
                                   columns=["paper_id", "disease_epoch", "authors_institutions", "text"],
                                   quoting=csv.QUOTE_NONE,
                                   escapechar='\\')
