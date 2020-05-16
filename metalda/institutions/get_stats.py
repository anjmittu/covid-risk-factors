import os
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


papers_table = pd.read_csv(os.path.join(PROJECT_ROOT, "data/mallet/institution/papers.csv"),
                           sep="\t",
                           names=["paper_id", "authors_institutions", "text"])


print("Number of unknown institutions: {}".format(len(papers_table[papers_table['authors_institutions'] == 'Unknown'])))
print("Number of papers: {}".format(len(papers_table)))