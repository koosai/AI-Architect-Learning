# Month8 L2：向量相似度  （对应 docs/08-rag/embeddings.mdx）
# 目标：余弦相似度 + top-k 排序——语义检索最核心的动作
# 用法：python labs/month08/m8l2_embeddings/test_embeddings.py
import math


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0


def top_k(query, docs, k):
    scored = [(name, cosine(query, vec)) for name, vec in docs]
    return [name for name, _ in sorted(scored, key=lambda x: -x[1])[:k]]


def run():
    assert abs(cosine([1, 0], [1, 0]) - 1) < 1e-9
    assert abs(cosine([1, 0], [0, 1])) < 1e-9
    docs = [("a", [1, 0, 0]), ("b", [0.9, 0.1, 0]), ("c", [0, 0, 1])]
    assert top_k([1, 0, 0], docs, 2) == ["a", "b"]
    print("✅ 全部通过: 余弦相似度 + top-k 排序")


if __name__ == "__main__":
    run()
