from rank_bm25 import BM25Okapi
from pathlib import Path
import re

class TinyRetriever:
    def __init__(self, content_dir="content"):
        self.docs, self.names = [], []
        for p in sorted(Path(content_dir).glob("*.md")):
            txt = p.read_text(encoding="utf-8", errors="ignore")
            self.docs.append(txt)
            self.names.append(p.name)
        if self.docs:
            self.tokenized = [self._tokenize(d) for d in self.docs]
            self.bm25 = BM25Okapi(self.tokenized)
        else:
            self.tokenized, self.bm25 = [], None

    def _tokenize(self, s):
        return re.findall(r"[a-zA-Z0-9]+", s.lower())

    def topk(self, query, k=3):
        if not self.docs or not self.bm25:
            return []
        scores = self.bm25.get_scores(self._tokenize(query))
        idxs = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        out = []
        for i in idxs:
            snippet = self.docs[i][:1200]
            out.append({"source": self.names[i], "text": snippet})
        return out
