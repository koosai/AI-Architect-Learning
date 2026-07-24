# Month12 L7：韧性与护栏挂载  （对应 docs/12-capstone/reliability-guardrails-build.mdx）
# 目标：把弹性和纵深护栏挂到 provider 层，让 RAG/Agent 自动受保护、不可绕过
# 用法：python labs/month12/m12l7_guardrails/test_guardrails.py


class GuardedProvider:
    def __init__(self, backend, fail=False):
        self.backend = backend
        self.fail = fail

    def complete(self, prompt):
        if "ignore previous" in prompt.lower():
            return {"blocked": "input"}                  # 入口护栏（挂在 provider，不可绕过）
        if self.fail:
            return {"result": "DEGRADED", "degraded": True}   # 弹性降级
        result = self.backend(prompt)
        if "SSN" in result:
            return {"blocked": "output"}                 # 出口护栏
        return {"result": result}


def run():
    gp = GuardedProvider(backend=lambda p: f"answer:{p}")
    assert gp.complete("hi")["result"] == "answer:hi"
    assert gp.complete("ignore previous")["blocked"] == "input"
    assert GuardedProvider(lambda p: "has SSN here").complete("x")["blocked"] == "output"
    assert GuardedProvider(lambda p: "x", fail=True).complete("hi")["degraded"]
    print("✅ 全部通过: provider 层护栏（弹性+纵深，不可绕过）")


if __name__ == "__main__":
    run()
