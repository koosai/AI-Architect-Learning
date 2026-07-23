# Month8 L6：重排  （对应 docs/08-rag/reranking.mdx）
# 目标：高召回 + 精重排，体会两阶段如何兼顾速度和精度，召回率为何是前提
# 用法：python labs/month08/m8l6_rerank/test_rerank.py


def two_stage(query_terms, docs, recall_k, final_k):
    # 阶段1：便宜的召回（词重叠计数），取 recall_k
    def overlap(d):
        return len(set(query_terms) & set(d["text"].split()))
    recalled = sorted(docs, key=lambda d: -overlap(d))[:recall_k]
    # 阶段2：精排（更强信号：命中词加权）
    def precise(d):
        return sum(2 if t in d["text"] else 0 for t in query_terms)
    reranked = sorted(recalled, key=lambda d: -precise(d))[:final_k]
    return [d["id"] for d in reranked]


def run():
    docs = [
        {"id": "a", "text": "cat sat mat"},
        {"id": "b", "text": "dog ran far"},
        {"id": "c", "text": "cat cat cat"},
        {"id": "d", "text": "bird flew"},
    ]
    out = two_stage(["cat", "sat"], docs, recall_k=3, final_k=2)
    assert "a" in out and len(out) == 2    # a 同时含 cat 和 sat，精排居首
    print("✅ 全部通过: 两阶段 高召回+精重排")


if __name__ == "__main__":
    run()
