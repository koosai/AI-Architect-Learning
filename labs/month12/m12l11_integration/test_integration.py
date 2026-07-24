# Month12 L11：端到端集成  （对应 docs/12-capstone/integration-e2e.mdx）
# 目标：组件组装成 Assistant 门面，两个核心用例端到端跑通，smoke test 守住整体
# 用法：python labs/month12/m12l11_integration/test_integration.py


class Assistant:
    def __init__(self):
        self.kb = {"raft": "raft uses leader election"}

    def rag_qa(self, q):
        for k, v in self.kb.items():
            if k in q:
                return {"answer": v, "cite": k}
        return {"abstain": True}

    def review(self, code):
        issues = []
        if "eval(" in code:
            issues.append("dangerous_eval")
        return {"issues": issues}


def smoke_test(assistant):
    r1 = assistant.rag_qa("how does raft work")
    r2 = assistant.review("x=eval(input())")
    return (not r1.get("abstain")) and "dangerous_eval" in r2["issues"]


def run():
    a = Assistant()
    assert a.rag_qa("raft?")["cite"] == "raft"               # 用例1：RAG
    assert a.review("eval(x)")["issues"] == ["dangerous_eval"]  # 用例2：评审
    assert a.rag_qa("unknown topic")["abstain"]
    assert smoke_test(a) is True                             # smoke 守住整体可用
    print("✅ 全部通过: Assistant 门面（两用例 e2e + smoke test）")


if __name__ == "__main__":
    run()
