import os
from data.data_utils import disease_epoch_intervals, get_disease_epoch
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

result = {}

with open(os.path.join(PROJECT_ROOT, "mallet-baseline/output/baseline_papers_keys.txt")) as f:
    output_keys = f.read()

number_topics = len(output_keys.split("\n"))-1

result[0] = {i: 0 for i in range(number_topics)}
for interval in disease_epoch_intervals:
    result[disease_epoch_intervals[interval]["epoch"]] = {i: 0 for i in range(number_topics)}


metadata_table = pd.read_csv(os.path.join(PROJECT_ROOT, "data/cord-19/metadata.csv"))
article_metadata = {row["sha"]: row for index, row in metadata_table.iterrows()}

with open(os.path.join(PROJECT_ROOT, "mallet-baseline/output/baseline_papers_compostion.txt")) as f:
    topic_results = f.read()

topic_results_dict = {}
for d in topic_results.split("\n"):
    composition = d.split("\t", 2)
    if len(composition) > 2:
        a_meta = article_metadata.get(composition[1], {})
        pub_date_str = a_meta.get("publish_time")
        disease_epoch = get_disease_epoch(pub_date_str)
        for i, topic_percent in enumerate(composition[2].split("\t")):
            result[disease_epoch][i] += float(topic_percent)

for e in result:
    print("The top topics for epoch {}".format(e))
    for k, v in sorted(result[e].items(), key=lambda item: item[1]):
        print("{}: {}".format(k,v))
    print(" ")