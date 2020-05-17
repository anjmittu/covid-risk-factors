# Metalda with Epoch labels

You can then run a quick preprocessing script to make this aligned with what Mallet is expecting as input.  You can run 
scripts `metalda/preprocess_papers_epoch.py` for epoch labelling or `metalda/preprocess_papers.py` to process data for 
all variations of MetaLDA.
```
$ cd metalda/epochs
$ python3 ../preprocess_papers.py OR python3 preprocess_papers_epoch.py
```

Resulting files should live in `./data/epoch`, please double check that this is the case.

Once you're in the docker container, you should have all the requisite Java dependencies to run Mallet.  You can either
run the exec script
```
$ ./exec.sh
```
