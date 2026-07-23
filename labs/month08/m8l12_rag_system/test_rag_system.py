# Month8 L12：可靠 RAG 系统  （对应 docs/08-rag/capstone-rag.mdx）
# 目标：检索准、权限安全、答案可信、能弃答——串成一个可靠 RAG
# 用法：python labs/month08/m8l12_rag_system/test_rag_system.py
import math


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0


class RAGSystem:
    def __init__(self, docs):
        self.docs = docs

    def answer(self, query_vec, user_perms, k=2, min_sim=0.5):
        cand = [d for d in self.docs if d["acl"] in user_perms]        # 权限过滤
        scored = sorted(cand, key=lambda d: -cosine(query_vec, d["vec"]))
        top = [d for d in scored[:k] if cosine(query_vec, d["vec"]) >= min_sim]
        if not top:
            return {"abstain": True}                                    # 不够相关 -> 弃答
        return {"abstain": False, "answer": top[0]["text"], "cite": top[0]["id"]}


def run():
    docs = [
        {"id": "a", "vec": [1, 0], "text": "sky is blue", "acl": "public"},
        {"id": "b", "vec": [0, 1], "text": "secret data", "acl": "secret"},
    ]
    r = RAGSystem(docs)
    ans = r.answer([1, 0], {"public"})
    assert not ans["abstain"] and ans["cite"] == "a"       # 检索准 + 权限安全 + 可信引用
    ans2 = r.answer([0.3, 0.3], {"public"}, min_sim=0.99)
    assert ans2["abstain"]                                  # 相关度不足 -> 能弃答
    print("✅ 全部通过: 可靠 RAG（检索准/权限安全/答案可信/能弃答）")


if __name__ == "__main__":
    run()
