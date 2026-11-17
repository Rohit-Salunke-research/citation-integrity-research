import re, math
from collections import Counter
import numpy as np

TOKEN_RE = re.compile(r"[a-z0-9]{2,}")

def tokenize(text):
    return TOKEN_RE.findall(str(text).lower())

class SentenceIndex:
    def __init__(self, sentences):
        self.sentences = sentences
        self.tokens = [tokenize(s["text"]) for s in sentences]

    def tfidf(self, query, k=10):
        # Word unigram TF-IDF; sublinear TF; smooth IDF; L2 normalization.
        docs = [s["text"] for s in self.sentences]
        if not docs:
            return []
        all_text = docs + [query]
        token_lists = [tokenize(x) for x in all_text]
        n = len(all_text)
        df = Counter()
        for terms in token_lists:
            df.update(set(terms))
        vectors = []
        for terms in token_lists:
            tf = Counter(terms)
            vec = {t: (1.0 + math.log(freq)) *
                   (math.log((1.0 + n) / (1.0 + df[t])) + 1.0)
                   for t, freq in tf.items()}
            norm = math.sqrt(sum(v*v for v in vec.values()))
            if norm:
                vec = {t: v / norm for t, v in vec.items()}
            vectors.append(vec)
        qv = vectors[-1]
        scores = []
        for i, vec in enumerate(vectors[:-1]):
            scores.append(sum(w * vec.get(t, 0.0) for t, w in qv.items()))
        order = np.argsort(-np.asarray(scores), kind="stable")[:k]
        return [(int(i), float(scores[i])) for i in order]

    def bm25(self, query, k=10):
        # Okapi BM25: k1=1.5, b=0.75.
        n_docs = len(self.tokens)
        if n_docs == 0:
            return []
        avgdl = sum(map(len, self.tokens)) / n_docs
        if avgdl == 0:
            return [(i, 0.0) for i in range(min(k, n_docs))]
        df = Counter()
        tfs = []
        for terms in self.tokens:
            tf = Counter(terms)
            tfs.append(tf)
            df.update(tf.keys())
        scores = [0.0] * n_docs
        for term in tokenize(query):
            dft = df.get(term, 0)
            if not dft:
                continue
            idf = math.log(1.0 + (n_docs - dft + 0.5) / (dft + 0.5))
            for i, tf in enumerate(tfs):
                f = tf.get(term, 0)
                if not f:
                    continue
                dl = len(self.tokens[i])
                denom = f + 1.5 * (1.0 - 0.75 + 0.75 * dl / avgdl)
                scores[i] += idf * f * 2.5 / denom
        order = np.argsort(-np.asarray(scores), kind="stable")[:k]
        return [(int(i), float(scores[i])) for i in order]
