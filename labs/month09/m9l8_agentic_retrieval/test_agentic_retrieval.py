# Month9 L8：Agentic 检索  （对应 docs/09-agent-architectures/agentic-retrieval.mdx）
# 目标：自主决定检索策略——把 M8 的检索变成 Agent 的工具
# 用法：python labs/month09/m9l8_agentic_retrieval/test_agentic_retrieval.py


def decide_strategy(query):
    if "vs" in query or "compare" in query:
        return "multi_query"          # 比较类 -> 多查询
    if len(query.split()) <= 2:
        return "direct"               # 简单 -> 直接检索
    return "rewrite"                  # 复杂 -> 先改写


def agentic_retrieve(query, retriever):
    strategy = decide_strategy(query)
    if strategy == "multi_query":
        return retriever(query + " A") + retriever(query + " B")
    if strategy == "rewrite":
        return retriever("refined: " + query)
    return retriever(query)


def run():
    assert decide_strategy("A vs B") == "multi_query"
    assert decide_strategy("cat") == "direct"
    assert decide_strategy("how does raft handle partition") == "rewrite"
    assert agentic_retrieve("cat", lambda q: [q]) == ["cat"]
    print("✅ 全部通过: Agentic 检索（自主决定检索策略）")


if __name__ == "__main__":
    run()
