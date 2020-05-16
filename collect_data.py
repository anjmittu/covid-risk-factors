"""
Script to pull out data from https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge
and convert it into a json lines file for use by the scholar topic model

NOTE: the extracted data from Kaggle should be put into a directory called 'covid_data'
"""

from collections import defaultdict
import csv
import datetime
import json
import os
import spacy

# NOTE: epoch 0 is the 'undefined' date time
disease_epoch_intervals = {
    "pre_sars": {
        "start": datetime.date(1900, 1, 1),
        "end": datetime.date(2002, 11, 27),
        "epoch": 1
    },
    "pre_mers": {
        "start": datetime.date(2002, 11, 28),
        "end": datetime.date(2012, 6, 1),
        "epoch": 2
    },
    "pre_covid": {
        "start": datetime.date(2012, 6, 2),
        "end": datetime.date(2019, 12, 1),
        "epoch": 3
    },
    "post_covid": {
        "start": datetime.date(2019, 12, 2),
        "end": datetime.date(2100, 1, 1),
        "epoch": 4
    }
}


def clean_text(text_blocks):
    """
    text_blocks: list of dict objects [{}, {}], each with the 'text' property
    """
    if not text_blocks:
        return ""
    full_text = " ".join(text_block.get("text").replace("\n", " ") for text_block in text_blocks)
    return full_text

def process_file(json_file, article_metadata):
    """
    Function to take in a single json object from the Covid dataset and
    extract some of the metadata we want and combine the text into a single
    string
    """
    authors = []
    authors_institutions = []
    metadata = json_file["metadata"]

    a_meta = article_metadata.get(json_file["paper_id"], {})    

    for author in json_file.get("metadata", {}).get("authors"):
        first = author.get("first")
        last = author.get("last")
        authors.append(f"{first} {last}")
        if author.get("affiliation", {}).get("institution"):
            authors_institutions.append(author.get("affiliation", {}).get("institution"))

    doc_text = clean_text(json_file.get("body_text"))

    # World's hackiest heuristic for removing non-english documents
    # It's virtually impossible for the word 'the' to not be used 
    # in a document of a certain length
    if "the" not in doc_text:
        return {}  

    
    pub_date_str = a_meta.get("publish_time")
    
    if not pub_date_str:
        pub_date = None
    elif len(pub_date_str) == 4:
        # Edge case where only the year is specified, we default to July 1 of that year to cut the year
        pub_date = datetime.date(int(pub_date_str), 7, 1)
    else:
        try:
            pub_date = datetime.datetime.strptime(pub_date_str, "%Y-%m-%d").date()
        except Exception as e:
            print("Odd date format ", pub_date_str)

    disease_epoch = 0

    if pub_date:
        for _epoch in disease_epoch_intervals:
            epoch = disease_epoch_intervals[_epoch]
            if pub_date >= epoch["start"] and pub_date <= epoch["end"]:
                disease_epoch = epoch["epoch"]

    top_authors_institution_counts = defaultdict(int)
    top_authors_institution = "unknown"
    for auth in authors_institutions:
        top_authors_institution_counts[auth] += 1

    top_count = 0
    for auth in top_authors_institution_counts:
        if top_authors_institution_counts[auth] > top_count:
            top_authors_institution = auth

    cleaned_doc = {
        "text": doc_text,
        "title": metadata.get("title"),
        "authors": authors,
        "authors_institutions": authors_institutions,
        "top_authors_institution": top_authors_institution,
        "abstract": clean_text(json_file.get("abstract")),
        "paper_id": json_file["paper_id"],
        "pub_date_str": pub_date_str,
        "disease_epoch": disease_epoch

    }
    
    return cleaned_doc

def collect_data():
    dir_path = os.path.dirname(os.path.realpath('__file__'))

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

    file_wiper = open("covid_data/combined_data.jsonl", "w+")
    file_wiper.close()

    csv_metadata_reader = csv.DictReader(open("covid_data/metadata.csv"))
    article_metadata = {row["sha"]: row for row in csv_metadata_reader}
    
    with open("covid_data/combined_data.jsonl", "a+") as output:
        for _dir in directories:
            print(f"Processing {_dir}")
            full_path = f"{dir_path}/covid_data/{_dir}/{_dir}"
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