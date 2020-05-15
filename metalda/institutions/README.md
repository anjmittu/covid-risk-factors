# Metalda with Institution labels

## Run a topic model on only the full papers
Prepare the data
```
$ cd metalda/institution
$ python3 ../preprocess_papers.py
$ mallet import-file \
    --input ../../data/mallet/institution/papers.csv \
    --output ../../data/mallet/institution/institution_papers.mallet \
    --remove-stopwords --keep-sequence --label-as-features --line-regex '([^\t]+)\t([^\t]+)\t(.*)'
$ java -cp /opt/MetaLDA/target/metalda-0.1-jar-with-dependencies.jar topicmodels.BinariseWordEmbeddings \
    --train-docs ../../data/mallet/institution/institution_papers.mallet \
    --input ../../data/embeddings/glove.6B.300d.txt \
    --output ../../data/mallet/institution/institution_embedding.txt
```

Run the model
```
$ java -Xmx8000m -cp /opt/MetaLDA/target/metalda-0.1-jar-with-dependencies.jar topicmodels.MetaLDATrain \
    --train-docs ../../data/mallet/institution/institution_papers.mallet \
    --num-topics 30 \
    --word-features ../../data/mallet/institution/institution_embedding.txt \
    --save-folder output/outputs_a0_b0_2 \
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
$ python ../../data/evaluate_results.py -p metalda/institutions/output/outputs_a0_b0_2/topic_words.txt -e data/embeddings/glove.6B.50d.txt
$ python ../../data/topic_coherence.py -p metalda/institutions/output/outputs_a0_b0_2/topic_words.txt
```
