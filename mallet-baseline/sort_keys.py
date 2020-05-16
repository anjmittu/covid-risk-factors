import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

results = {}

with open(os.path.join(PROJECT_ROOT, "mallet-baseline/output/baseline_papers_keys.txt")) as f:
    output_keys = f.read()

for k in output_keys.split("\n"):
    items = k.split("\t")
    if len(items) > 2:
        results[items[1]] = [items[0], items[2]]

for k in sorted(results.keys(), reverse=True):
    print("{} {} {}".format(results[k][0], k, results[k][1]))

