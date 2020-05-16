import pickle
from gensim.test.utils import datapath
from cord_19 import CorpusCord19
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

corpus = CorpusCord19(datapath(os.path.join(PROJECT_ROOT, "data/metalda/institution/papers.csv")))

pickle.dump(corpus, open("corpus.p", "wb"))
