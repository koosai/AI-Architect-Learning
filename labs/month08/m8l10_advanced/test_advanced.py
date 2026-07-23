# Month8 L10：高级 RAG  （对应 docs/08-rag/advanced-rag.mdx）
# 目标：权限/时效过滤 + 多跳串联——高级 RAG 里最该先有的两个能力
# 用法：python labs/month08/m8l10_advanced/test_advanced.py


def filtered_search(docs, user_perms, now):
    return [d["id"] for d in docs
            if d["acl"] in user_perms and d["valid_until"] >= now]   # 权限 + 时效


def multi_hop(start, kb, hops=2):
    chain = [start]
    cur = start
    for _ in range(hops):
        nxt = kb.get(cur)
        if not nxt:
            break
        chain.append(nxt)
        cur = nxt
    return chain


def run():
    docs = [
        {"id": "a", "acl": "public", "valid_until": 10},
        {"id": "b", "acl": "secret", "valid_until": 10},
        {"id": "c", "acl": "public", "valid_until": 1},
    ]
    assert filtered_search(docs, {"public"}, now=5) == ["a"]   # b 无权限、c 过期
    kb = {"paris": "france", "france": "europe"}
    assert multi_hop("paris", kb, hops=2) == ["paris", "france", "europe"]
    print("✅ 全部通过: 权限/时效过滤 + 多跳串联")


if __name__ == "__main__":
    run()
