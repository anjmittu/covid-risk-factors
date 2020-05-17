# covid-risk-factors
Comparing different topic models to see if covid-19 risk factors can be identified as one of the latent topics

Build docker image:
```
$ docker build -t covid_risk_factors .
```

Run the docker image
```
$ docker run -it --rm -v `pwd`:/usr/src/myapp -w /usr/src/myapp covid_risk_factors
```

Note: Before running, download the data from https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge and
place it in the directory `covid-risk-factors/data/cord-19/`

More information on how to run each model can be found under it's directory:
* Mallet baseline: `mallet-baseline/`
* MetaLDA with institutions: `metaLDA/institutions/`
* MetaLDA with epochs: `metaLDA/institutions/`

You can then run a quick preprocessing script to make this aligned with what Mallet is expecting as input.
You can run scripts `metalda/preprocess_papers_epoch.py` for epoch labelling or `metalda/preprocess_papers.py` for institutional labelling.
`python3 metalda/preprocess_papers_epoch.py` and `python3 metalda/preprocess_papers.py`
Resulting files should live in `./data/epoch_mallet_inputs` for epochs and `data/mallet/papers.csv` for institutions, please double check that this is the case.

Once you're in the docker container, you should have all the requisite Java dependencies to run Mallet.
```
$ ./exec.sh
```

