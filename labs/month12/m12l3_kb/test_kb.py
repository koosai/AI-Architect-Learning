# Month12 L3：知识库构建  （对应 docs/12-capstone/knowledge-base-build.mdx）
# 目标：摄取→分块→embedding→向量库→检索跑通，返回带引用的相关片段
# 用法：python labs/month12/m12l3_kb/test_kb.py
import math


def chunk(text, size):
    words = text.split()
    return [" ".join(words[i:i + size]) for i in range(0, len(words), size)]


def embed(text):
    v = [0, 0, 0]                        # 玩具 embedding：词哈希入 3 桶
    for w in text.split():
        v[hash(w) % 3] += 1
    return v


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0


class KB:
    def __init__(self):
        self.chunks = []

    def ingest(self, doc_id, text, size=3):
        for i, c in enumerate(chunk(text, size)):
            self.chunks.append({"id": f"{doc_id}#{i}", "text": c, "vec": embed(c)})

    def retrieve(self, query, k=2):
        qv = embed(query)
        ranked = sorted(self.chunks, key=lambda c: -cosine(qv, c["vec"]))
        return [{"id": c["id"], "text": c["text"]} for c in ranked[:k]]


def run():
    kb = KB()
    kb.ingest("d1", "the cat sat on the mat and the dog ran")
    res = kb.retrieve("cat", k=1)
    assert len(res) == 1 and "#" in res[0]["id"]     # 返回带引用 id 的片段
    print("✅ 全部通过: 知识库（摄取→分块→embedding→检索，带引用）")


if __name__ == "__main__":
    run()
