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

## SCHOLAR
Code in `scholar` taken from https://github.com/dallascard/scholar.

Python requirements
```
python3
pytorch 0.4
numpy
scipy
pandas
gensim
```

Scholar requires data being in a jsonlines format. The script `data/collect_data.py` will transform the dataset download (which should be in the project's root directory) into a jsonlines files called `data/baseline/combined_data.json`

Scholar then requires some preprocessing on top of the json lines file
`python scholar/preprocess_data.py data/baseline/combined_data.json data/scholar/processed/ --vocab-size 2000 --label disease_epoch,top_authors_institution`

Then to run the scholar model itself (this example runs the model with both metadata attributes as covariates)
`python run_scholar.py data/scholar/processed/ -k 30 -o results/output_smallV_30_both --topic-covars disease_epoch,top_authors_institution`

