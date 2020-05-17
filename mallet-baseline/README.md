# Mallet Baseline

## Run a topic model on only the full papers
```
$ cd mallet-baseline
$ python3 preprocess_papers.py
$ mallet import-file --input ../data/mallet/papers.csv --output baseline_papers.mallet --label 0 --data 4 --remove-stopwords --keep-sequence --line-regex '([^\t]+)\t([^\t]+)\t([^\t]+)\t(.*)'
```

Run the model
Note you may need to increase the memory inside mallet script, found here `/usr/lib/mallet-2.0.8/bin/mallet`
```
$ mallet train-topics  \
    --input baseline_papers.mallet \
    --num-topics 30 \
    --output-state output/baseline_papers_topic_state.gz \
    --output-topic-keys output/baseline_papers_keys.txt \
    --output-doc-topics output/baseline_papers_compostion.txt \
    --optimize-interval 10 \
    --num-top-words 100 \
    --num-iterations 2000 \
    --num-threads 16
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
$ python ../data/evaluate_results.py -p mallet-baseline/output/topic_words.txt -e data/embeddings/glove.6B.50d.txt
```

To find the UMass score, run the topic_coherence.py script in the data directory
``
$ python topic_coherence.py -p mallet-baseline/output/topic_words.txt
``

