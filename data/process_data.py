"""
Script to pull out data from https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge
and convert it into a json lines file for use by the scholar topic model
NOTE: the extracted data from Kaggle should be put into a directory called 'covid_data'
"""
import csv
import json
import os
from data.data_utils import process_file

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def collect_data():
    directories = {
        "comm_use_subset": "",
        "biorxiv_medrxiv": "",
        "noncomm_use_subset": "",
        "custom_license": ""
    }
    ex = {}
    total = 0
    total_with_authors = 0
    total_with_abstracts = 0
    non_eng = 0
    file_wiper = open(os.path.join(PROJECT_ROOT, "data/baseline/combined_data.json"), "w+")
    file_wiper.close()
    with open(os.path.join(PROJECT_ROOT, "data/cord-19/metadata.csv")) as f:
        csv_metadata_reader = csv.DictReader(f)
        article_metadata = {row["sha"]: row for row in csv_metadata_reader}
    with open(os.path.join(PROJECT_ROOT, "data/baseline/combined_data.json"), "a+") as output:
        for _dir in directories:
            print(f"Processing {_dir}")
            full_path = os.path.join(PROJECT_ROOT, "data/cord-19/{0}/{0}".format(_dir))
            subdirs = os.listdir(full_path)
            for sub_dir in subdirs:
                # NOTE: The PMC_JSON files do not have author information in them
                # We are going to skip these for now
                if sub_dir == "pmc_json":
                    print("Skipping PMC JSON Dir...")
                    continue
                print(f"Processing sub dir {sub_dir}")
                sub_path = full_path + f"/{sub_dir}"
                files = os.listdir(sub_path)
                for _file in files:
                    file_path = sub_path + f"/{_file}"
                    json_file = json.load(open(file_path))
                    clean_file = process_file(json_file, article_metadata)
                    # Handle the case of a non english document
                    if clean_file:
                        if clean_file["authors_institutions"]:
                            total_with_authors += 1
                        if clean_file["abstract"]:
                            total_with_abstracts += 1
                        output.write("{}\n".format(json.dumps(clean_file)))
                    else:
                        non_eng += 1
                    total += 1
                    if (total % 1000) == 0:
                        print(f"Total {total} , with authors {total_with_authors}, with abstracts {total_with_abstracts}, Non English Documents removed {non_eng}")


if __name__ == "__main__":
    print("Starting...")
    collect_data()