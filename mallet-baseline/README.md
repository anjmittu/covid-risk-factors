# Mallet Baseline

Build docker image:
```
$ docker build -t covid_mallet_baseline .
```

Run the docker image
```
$ docker run -it --rm -v $(dirname `pwd`):/usr/src/myapp -w /usr/src/myapp covid_mallet_baseline
```

Prepare the data
```
$ cd mallet-baseline
$ python3 preprocess_data.py
$ mallet import-file --input ../data/baseline/abstracts.csv --output baseline_abstracts.mallet --label 0 --data 2 --remove-stopwords --keep-sequence
```

Run the model
```
$ mallet train-topics  --input baseline_abstracts.mallet --num-topics 20
```
