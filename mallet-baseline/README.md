# Mallet Baseline

Build docker image:
```
$ docker build -t covid_mallet_baseline .
```

Run the docker image
```
$ docker run -it --rm -v $(dirname `pwd`):/usr/src/myapp -w /usr/src/myapp covid_mallet_baseline
```

Note: Before running, download the data from https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge and
place it in the directory `covid-risk-factors/data/cord-19/`


## Run a topic model on only the abstracts
Prepare the data
```
$ cd mallet-baseline
$ python3 preprocess_abstracts.py
$ mallet import-file --input ../data/baseline/abstracts.csv --output baseline_abstracts.mallet --label 0 --data 2 --remove-stopwords --keep-sequence
```

Run the model
```
$ mallet train-topics  --input baseline_abstracts.mallet --num-topics 20
```

## Run a topic model on only the full papers
```
$ cd mallet-baseline
$ python3 preprocess_papers.py
$ mallet import-file --input ../data/baseline/papers.csv --output baseline_papers.mallet --label 0 --data 2 --remove-stopwords --keep-sequence
```

Run the model
```
$ mallet train-topics  --input baseline_papers.mallet --num-topics 20 --output-state output/baseline_papers_topic_state.gz --output-topic-keys output/baseline_papers_keys.txt --output-doc-topics output/baseline_papers_compostion.txt --optimize-interval 20
```
