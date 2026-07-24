# Month8 L5：混合检索  （对应 docs/08-rag/hybrid-search.mdx）
# 目标：稠密 + 稀疏两路检索 + RRF 融合——生产 RAG 的常见召回层
# 用法：python labs/month08/m8l5_hybrid/test_hybrid.py


def rrf(rankings, k=60):
    # Reciprocal Rank Fusion：score = Σ 1/(k + rank)
    scores = {}
    for ranking in rankings:
        for rank, doc in enumerate(ranking):
            scores[doc] = scores.get(doc, 0) + 1 / (k + rank + 1)
    return [d for d, _ in sorted(scores.items(), key=lambda x: -x[1])]


def run():
    dense = ["a", "b", "c"]    # 稠密（语义）排序
    sparse = ["b", "a", "d"]   # 稀疏（BM25）排序
    fused = rrf([dense, sparse])
    assert set(fused[:2]) == {"a", "b"}   # 两路都靠前的 a、b 融合后居首
    assert "c" in fused and "d" in fused
    print("✅ 全部通过: 稠密+稀疏两路 + RRF 融合")


if __name__ == "__main__":
    run()
