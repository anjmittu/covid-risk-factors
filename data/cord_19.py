from gensim.corpora.textcorpus import TextCorpus
from nltk.corpus import stopwords
from gensim import utils


class CorpusCord19(TextCorpus):
    stopwords = set(stopwords.words('english'))

    def get_texts(self):
        for doc in self.getstream():
            yield [word for word in utils.to_unicode(doc).split("\t")[2].lower().split() if word not in self.stopwords]

    def __len__(self):
        self.length = sum(1 for _ in self.get_texts())
        return self.length
