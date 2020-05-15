# Metalda with epoch labels

## Run a topic model on only the full papers
Prepare the data
```
$ cd metalda/epochs
$ python3 ../preprocess_papers.py
$ mallet import-file \
    --input ../../data/metalda/epoch/papers.csv \
    --output ../../data/metalda/epoch/epoch_papers.mallet \
    --remove-stopwords --keep-sequence --label-as-features --line-regex '([^\t]+)\t([^\t]+)\t(.*)'
$ java -cp /opt/MetaLDA/target/metalda-0.1-jar-with-dependencies.jar topicmodels.BinariseWordEmbeddings \
    --train-docs ../../data/metalda/epoch/epoch_papers.mallet \
    --input ../../data/embeddings/glove.6B.300d.txt \
    --output ../../data/metalda/epoch/epoch_embedding.txt
```

Run the model
```
$ java -Xmx8000m -cp /opt/MetaLDA/target/metalda-0.1-jar-with-dependencies.jar topicmodels.MetaLDATrain \
    --train-docs ../../data/metalda/epoch/epoch_papers.mallet \
    --num-topics 30 \
    --word-features ../../data/metalda/epoch/epoch_embedding.txt \
    --save-folder output/output_a0_b0 \
    --sample-alpha-method 0 \
    --sample-beta-method 0 \
    --num-threads 16
```

Run analysis on results
```
$ octave-cli analysis.m
```


Find the average cos sim
```
$ python ../../data/evaluate_results.py -p metalda/epochs/output/outputs_a0_b0/topic_words.txt
```
