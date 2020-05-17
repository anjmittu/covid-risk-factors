"""
Script to pull out data from https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge
and convert it into a json lines file for use by the scholar topic model
NOTE: the extracted data from Kaggle should be put into a directory called 'covid_data'
"""
import csv
import datetime
import json
import os, random
from data.data_utils import process_file, disease_epoch_intervals

def collect_data():
    dir_path = os.path.dirname(os.path.realpath('__file__'))
    directories = {
        "comm_use_subset": "",
        "biorxiv_medrxiv": "",
        "noncomm_use_subset": "",
        "custom_license": ""
    }
    mallet_inputs = "{}/../data/epoch/epoch_mallet_inputs".format(dir_path)
    for directory in list(map(lambda x: x['epoch'], disease_epoch_intervals.values())) + [0]:
        if os.path.exists("{mallet_inputs}/train/{directory}".format(mallet_inputs=mallet_inputs, directory=directory)):
            print("Already created directory; raising issue now")
            raise Exception("Already created dirs; raising issue now")
        else:
            os.makedirs("{mallet_inputs}/train/{directory}".format(mallet_inputs=mallet_inputs, directory=directory))

        if os.path.exists("{mallet_inputs}/test/{directory}".format(mallet_inputs=mallet_inputs, directory=directory)):
            print("Already created directory; raising issue now")
            raise Exception("Already created dirs; raising issue now")
        else:
            os.makedirs("{mallet_inputs}/test/{directory}".format(mallet_inputs=mallet_inputs, directory=directory))

    ex = {}
    total = 0
    total_with_authors = 0
    total_with_abstracts = 0
    non_eng = 0
    # file_wiper = open("covid_data/combined_data.jsonl", "w+")
    # file_wiper.close()
    csv_metadata_reader = csv.DictReader(open("../data/cord-19/metadata.csv"))
    article_metadata = {row["sha"]: row for row in csv_metadata_reader}
    # with open("covid_data/combined_data.jsonl", "a+") as output:
    for _dir in directories:
        print(f"Processing {_dir}")
        full_path = f"{dir_path}/../data/cord-19/{_dir}/{_dir}"
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
                    if random.randint(0,100) > 90:
                        with open("{mallet_inputs}/test.txt".format(disease_epoch=clean_file["disease_epoch"], mallet_inputs=mallet_inputs, dir=_dir, file=os.path.splitext(_file)[0]), "a") as f:
                            # f.write("{text}".format(paper_id=clean_file["paper_id"], disease_epoch=clean_file["disease_epoch"], text=clean_file["text"]))
                            # f.write("{paper_id}\t{disease_epoch}_{top_institution}\t{text}\n".format(paper_id=clean_file["paper_id"], top_institution=(None if len(clean_file["authors_institutions"]) < 1 else clean_file["authors_institutions"][0]),disease_epoch=clean_file["disease_epoch"], text=clean_file["text"]))
                            f.write("{paper_id}\t{disease_epoch}\t{text}\n".format(paper_id=clean_file["paper_id"], top_institution=(None if len(clean_file["authors_institutions"]) < 1 else clean_file["authors_institutions"][0]),disease_epoch=clean_file["disease_epoch"], text=clean_file["text"]))

                    else:
                        with open("{mallet_inputs}/train.txt".format(disease_epoch=clean_file["disease_epoch"], mallet_inputs=mallet_inputs, dir=_dir, file=os.path.splitext(_file)[0]), "a") as f:
                            f.write("{paper_id}\t{disease_epoch}\t{text}\n".format(paper_id=clean_file["paper_id"], top_institution=(None if len(clean_file["authors_institutions"]) < 1 else clean_file["authors_institutions"][0]),disease_epoch=clean_file["disease_epoch"], text=clean_file["text"]))

                    #     with open("{mallet_inputs}/train/{disease_epoch}/{file}_{dir}.txt".format(disease_epoch=clean_file["disease_epoch"], mallet_inputs=mallet_inputs, dir=_dir, file=os.path.splitext(_file)[0]), "w") as f:
                    #         f.write("{text}".format(paper_id=clean_file["paper_id"], disease_epoch=clean_file["disease_epoch"], text=clean_file["text"]))

                        # f.write("{paper_id}\t{disease_epoch}\t{text}\n".format(paper_id=clean_file["paper_id"], disease_epoch=clean_file["disease_epoch"], text=clean_file["text"]))

                    # output.write("{}\n".format(json.dumps(clean_file)))
                else:
                    non_eng += 1
                total += 1
                if (total % 1000) == 0:
                    print(f"Total {total} , with authors {total_with_authors}, with abstracts {total_with_abstracts}, Non English Documents removed {non_eng}")
if __name__ == "__main__":
    print("Starting...")
    collect_data()
