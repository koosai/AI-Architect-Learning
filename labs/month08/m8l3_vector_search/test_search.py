# Month8 L3：向量检索  （对应 docs/08-rag/vector-search.mdx）
# 目标：top-k 检索 + 召回率 + 元数据过滤
# 用法：python labs/month08/m8l3_vector_search/test_search.py
import math


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0


def search(query, docs, k, filter_fn=None):
    cand = [d for d in docs if (filter_fn is None or filter_fn(d["meta"]))]
    scored = sorted(cand, key=lambda d: -cosine(query, d["vec"]))
    return [d["id"] for d in scored[:k]]


def recall_at_k(retrieved, relevant):
    return len(set(retrieved) & set(relevant)) / len(relevant)


def run():
    docs = [
        {"id": "a", "vec": [1, 0], "meta": {"lang": "en"}},
        {"id": "b", "vec": [0.8, 0.2], "meta": {"lang": "zh"}},
        {"id": "c", "vec": [0, 1], "meta": {"lang": "en"}},
    ]
    assert search([1, 0], docs, 2) == ["a", "b"]
    assert search([1, 0], docs, 2, filter_fn=lambda m: m["lang"] == "en") == ["a", "c"]  # 元数据过滤
    assert recall_at_k(["a", "b"], ["a", "c"]) == 0.5
    print("✅ 全部通过: top-k检索 + 召回率 + 元数据过滤")


if __name__ == "__main__":
    run()
