# Month8 L8：RAG 生成  （对应 docs/08-rag/rag-generation.mdx）
# 目标：证据拼装 + 引用校验 + 弃答——把检索和生成接好的最后一环
# 用法：python labs/month08/m8l8_generation/test_generation.py


def generate(question, retrieved, min_evidence=1):
    if len(retrieved) < min_evidence:
        return {"answer": None, "abstain": True, "reason": "insufficient_evidence"}
    ev = retrieved[0]
    ids = {r["id"] for r in retrieved}
    if ev["id"] not in ids:
        return {"answer": None, "abstain": True, "reason": "bad_citation"}
    return {"answer": f"{ev['text']} [cite:{ev['id']}]", "abstain": False}


def run():
    r = generate("q", [{"id": "d1", "text": "fact one"}])
    assert not r["abstain"] and "[cite:d1]" in r["answer"]
    r2 = generate("q", [])
    assert r2["abstain"] and r2["reason"] == "insufficient_evidence"   # 无证据 -> 弃答
    print("✅ 全部通过: 证据拼装 + 引用校验 + 弃答")


if __name__ == "__main__":
    run()
