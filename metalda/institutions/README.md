# Mallet Baseline

## Run a topic model on only the full papers
Prepare the data
```
$ cd mallet-baseline
$ python3 preprocess_papers.py
$ mallet import-file \
    --input ../../data/metalda/institution/papers.csv \
    --output ../../data/metalda/institution/institution_papers.mallet \
    --remove-stopwords --keep-sequence --label-as-features
$ mallet split \
    --input ../../data/metalda/institution/institution_papers.mallet \
    --training-file ../../data/metalda/institution/institution_papers_train.mallet \
    --testing-file ../../data/metalda/institution/institution_papers_test.mallet \
    --training-portion .8
$ java -cp /opt/MetaLDA/target/metalda-0.1-jar-with-dependencies.jar topicmodels.BinariseWordEmbeddings \
    --train-docs ../../data/metalda/institution/institution_papers_train.mallet \
    --test-docs ../../data/metalda/institution/institution_papers_test.mallet \
    --input ../../data/embeddings/glove.6B.50d.txt \
    --output ../../data/metalda/institution/institution_embedding.txt
```

Run the model
```
$ java -Xmx8000m -cp /opt/MetaLDA/target/metalda-0.1-jar-with-dependencies.jar topicmodels.MetaLDATrain \
    --train-docs ../../data/metalda/institution/institution_papers_train.mallet \
    --num-topics 30 \
    --word-features ../../data/metalda/institution/institution_embedding.txt \
    --save-folder outputs/output_a0_b0_2 \
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
$ python ../../data/evaluate_results.py -p metalda/institutions/outputs_a0_b0/topic_words.txt
```
