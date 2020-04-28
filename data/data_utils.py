"""
Tools to process the data from https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge
"""

def clean_text(text_blocks):
    """
    text_blocks: list of dict objects [{}, {}], each with the 'text' property
    """
    if not text_blocks:
        return ""
    full_text = " ".join(text_block.get("text").replace("\n", " ") for text_block in text_blocks)
    return full_text


def process_file(json_file):
    """
    Function to take in a single json object from the Covid dataset and
    extract some of the metadata we want and combine the text into a single
    string
    """
    authors = []
    authors_institutions = []
    metadata = json_file["metadata"]
    for author in json_file.get("metadata", {}).get("authors"):
        first = author.get("first")
        last = author.get("last")
        authors.append(f"{first} {last}")
        authors_institutions.append(author.get("affiliation", {}).get("institution"))
    cleaned_doc = {
        "text": clean_text(json_file.get("body_text")),
        "title": metadata.get("title"),
        "authors": authors,
        "authors_institutions": authors_institutions,
        "abstract": clean_text(json_file.get("abstract")),
        "paper_id": json_file["paper_id"]
    }
    return cleaned_doc