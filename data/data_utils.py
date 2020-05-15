"""
Tools to process the data from https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge
"""

# NOTE: epoch 0 is the 'undefined' date time
import datetime
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

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


def get_disease_epoch(pub_date_str):

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
    return disease_epoch


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
    authors_institution = ""
    for a in authors_institutions:
        if len(a) > 0:
            authors_institution = a
            break
    if authors_institution == "":
        authors_institution = "Unknown"
    doc_text = clean_text(json_file.get("body_text"))
    # World's hackiest heuristic for removing non-english documents
    # It's virtually impossible for the word 'the' to not be used
    # in a document of a certain length
    try:
        if len(doc_text) < 10 or detect(doc_text[:1000]) != "en":
            return {}
    except LangDetectException:
        return {}
    pub_date_str = a_meta.get("publish_time")
    disease_epoch = get_disease_epoch(pub_date_str)
    cleaned_doc = {
        "text": doc_text,
        "title": metadata.get("title"),
        "authors": authors,
        "authors_institutions": authors_institution,
        "abstract": clean_text(json_file.get("abstract")),
        "paper_id": json_file["paper_id"],
        "pub_date_str": pub_date_str,
        "disease_epoch": disease_epoch
    }
    return cleaned_doc

