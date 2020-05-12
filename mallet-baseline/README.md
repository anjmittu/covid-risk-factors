# Mallet Baseline

## Run a topic model on only the full papers
```
$ cd mallet-baseline
$ python3 preprocess_papers.py
$ mallet import-file --input ../data/baseline/papers.csv --output baseline_papers.mallet --label 0 --data 2 --remove-stopwords --keep-sequence
```

Run the model
```
$ mallet train-topics  \
    --input baseline_papers.mallet \
    --num-topics 30 \
    --output-state output/baseline_papers_topic_state.gz \
    --output-topic-keys output/baseline_papers_keys.txt \
    --output-doc-topics output/baseline_papers_compostion.txt \
    --optimize-interval 10 \
    --num-top-words 100
```

Print out the top topics in order
```
$ python3 sort_keys.py
```

Print out the top topics associated with each epoch
```
$ python3 sort_by_time.py
```

Find the average cos sim
```
$ python ../data/evaluate_results.py -p mallet-baseline/output/topic_words.txt 
```

