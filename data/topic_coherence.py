import os
import argparse
from gensim.models.coherencemodel import CoherenceModel
import pickle
from gensim.corpora import Dictionary

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def evaluate(topics_path="mallet-baseline/output/topic_words.txt"):
    f = open(os.path.join(PROJECT_ROOT, topics_path))
    topics_text = f.read()
    topics_list = [line.split(" ")[:10] for line in topics_text.split("\n") if len(line) > 1]
    print("Topics read")

    corpus = pickle.load(open("corpus.p", "rb"))
    print("Read in corpus")
    with open(os.path.join(PROJECT_ROOT, "results/saved_30_topics_metalda_external_disease_epoch/train_alphabet.txt")) as f:
        wrds = [line for line in f.read().split("\n")]
    dct = Dictionary([wrds])
    print("Created dictionary")
    # text=corpus.get_texts()
    # print("Got text")

    cm = CoherenceModel(topics=topics_list, corpus=corpus, texts=corpus.get_texts(), dictionary=dct, coherence='u_mass')
    print("Model created")

    coherence_lda = cm.get_coherence()
    print('\nCoherence Score: ', coherence_lda)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluating output from topic model')
    parser.add_argument('-p', dest='topic_path', help='path to topic_words file')
    args = parser.parse_args()
    print("Starting...")
    evaluate(args.topic_path)
