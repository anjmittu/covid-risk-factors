import pandas as pd
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
metadata_table = pd.read_csv(os.path.join(PROJECT_ROOT, "data/cord-19/metadata.csv"))

# Drop articles missing an abstract
metadata_table = metadata_table.dropna(subset=['abstract'])

if not os.path.exists(os.path.join(PROJECT_ROOT, "data/baseline")):
    os.makedirs(os.path.join(PROJECT_ROOT, "data/baseline"))

metadata_table[['cord_uid','abstract']].to_csv(os.path.join(PROJECT_ROOT, "data/baseline/abstracts.csv"), sep=" ", header=False, index=False)
