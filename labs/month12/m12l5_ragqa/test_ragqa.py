# Month12 L5：RAG QA 核心用例  （对应 docs/12-capstone/rag-qa-build.mdx）
# 目标：检索接上生成，做出 grounding + 真引用 + 弃答的第一个核心用例
# 用法：python labs/month12/m12l5_ragqa/test_ragqa.py


def rag_qa(question, retrieved, min_sim=0.5):
    relevant = [r for r in retrieved if r["sim"] >= min_sim]
    if not relevant:
        return {"abstain": True, "reason": "no_grounding"}    # 无充分证据 -> 弃答
    top = relevant[0]
    return {"abstain": False, "answer": f"{top['text']} [cite:{top['id']}]", "cite": top["id"]}


def run():
    r = rag_qa("q", [{"id": "d1", "text": "sky is blue", "sim": 0.9}])
    assert not r["abstain"] and r["cite"] == "d1" and "[cite:d1]" in r["answer"]
    r2 = rag_qa("q", [{"id": "d1", "text": "x", "sim": 0.2}])
    assert r2["abstain"]
    print("✅ 全部通过: RAG QA（grounding+真引用+弃答）")


if __name__ == "__main__":
    run()
