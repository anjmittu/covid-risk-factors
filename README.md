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
* MetaLDA with epochs: `metaLDA/epochs/`


