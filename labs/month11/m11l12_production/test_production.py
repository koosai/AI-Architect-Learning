# Month11 L12：生产级 AI 应用  （对应 docs/11-production-ai-platform/capstone-ai-platform.mdx）
# 目标：把 Month 11 全部能力经模型网关整合，完成一个“能上生产”的 AI 应用
# 用法：python labs/month11/m11l12_production/test_production.py


class ProductionApp:
    def __init__(self):
        self.budget = 10
        self.trace = []

    def answer(self, question, context, difficulty=0.5):
        # 网关收口：输入护栏 -> 成本 -> 证据/弃答 -> 观测
        if "ignore previous" in question.lower():
            return {"status": "blocked_input"}
        cost = 3 if difficulty >= 0.7 else 1
        if cost > self.budget:
            return {"status": "over_budget"}
        self.budget -= cost
        if not context:
            self.trace.append("abstain")
            return {"status": "abstain", "reason": "no_context"}   # 无证据弃答
        self.trace.append("answered")
        return {"status": "ok", "answer": f"{context} [cited]"}


def run():
    app = ProductionApp()
    r = app.answer("what color", "sky is blue")
    assert r["status"] == "ok" and "[cited]" in r["answer"]
    r2 = app.answer("q", "")
    assert r2["status"] == "abstain"
    r3 = app.answer("ignore previous", "x")
    assert r3["status"] == "blocked_input"
    assert app.trace == ["answered", "abstain"]
    print("✅ 全部通过: 生产级 AI 应用（网关收口: 护栏/成本/弃答/观测）")


if __name__ == "__main__":
    run()
