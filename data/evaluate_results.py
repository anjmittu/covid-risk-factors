from scipy.spatial.distance import cosine
import os
import argparse


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

"""
Function to evaluate topic results with custome selected embeddings
"""
def load_embeddings(embeddings_path):
    f = open(embeddings_path)
    embeddings_dict = {}
    for line in f.readlines():
        split_line = line.replace("\n", "").split(" ")
        word = split_line[0]
        weights = split_line[1:]
        weights = [float(weight) for weight in weights]
        embeddings_dict[word] = weights
    return embeddings_dict


def calculate_topic_avg_cosine(topic_terms, embeddings_dict):
    total_sim = 0
    found_pairs = 0
    for i in range(0, len(topic_terms)):
        for j in range(i, len(topic_terms)):
            term_i = topic_terms[i]
            term_j = topic_terms[j]
            if embeddings_dict.get(term_i) and embeddings_dict.get(term_j):
                cos_sim = cosine(embeddings_dict.get(term_i), embeddings_dict.get(term_j))
                total_sim += cos_sim
                found_pairs += 1
    return total_sim/found_pairs


def evaluate(topics_path="mallet-baseline/output/topic_words.txt",
             embeddings_dict=None,
             embeddings_path="data/embeddings/glove.6B.50d.txt",
             n=10):
    if not embeddings_dict:
        embeddings_dict = load_embeddings(os.path.join(PROJECT_ROOT, embeddings_path))
    f = open(os.path.join(PROJECT_ROOT, topics_path))
    topics_text = f.read()
    # NOTE: n is the number of top words to consider. Scholar will list the top 100 terms
    # however our vocab may be too small to even encompass that
    topics_list = [line.split(" ") for line in topics_text.split("\n")]
    in_vocab = 0
    total_vocab = 0
    out_vocab = 0
    for topic in topics_list:
        for term in topic[:n]:
            total_vocab += 1
            if embeddings_dict.get(term):
                in_vocab += 1
            else:
                out_vocab += 1
    print(f"Total {total_vocab}, In {in_vocab}, Out: {out_vocab}")
    cos_sims = []
    for topic in topics_list:
        cos_sims.append(calculate_topic_avg_cosine(topic, embeddings_dict))
    print(f"Average Cos Sim {sum(cos_sims)/len(cos_sims)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluating output from topic model')
    parser.add_argument('-p', dest='topic_path', help='path to topic_words file')
    args = parser.parse_args()
    print("Starting...")
    evaluate(args.topic_path)