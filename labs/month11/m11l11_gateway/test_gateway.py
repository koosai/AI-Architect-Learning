# Month11 L11：模型网关  （对应 docs/11-production-ai-platform/ai-platform-architecture.mdx）
# 目标：把路由/护栏/成本/观测横切能力收口进一个统一的模型网关
# 用法：python labs/month11/m11l11_gateway/test_gateway.py


class ModelGateway:
    def __init__(self, budget=10):
        self.budget = budget
        self.trace = []

    def handle(self, request):
        # 收口：输入护栏 -> 路由 -> 成本 -> 观测
        if "ignore previous" in request["prompt"].lower():
            return {"blocked": "input_guard"}
        model = "expensive" if request.get("difficulty", 0) >= 0.7 else "cheap"
        cost = 5 if model == "expensive" else 1
        if cost > self.budget:
            return {"blocked": "budget"}
        self.budget -= cost
        self.trace.append({"model": model, "cost": cost})   # 观测
        return {"ok": True, "model": model, "remaining_budget": self.budget}


def run():
    gw = ModelGateway(budget=10)
    r = gw.handle({"prompt": "hi", "difficulty": 0.9})
    assert r["model"] == "expensive" and r["remaining_budget"] == 5
    r2 = gw.handle({"prompt": "ignore previous", "difficulty": 0.1})
    assert r2["blocked"] == "input_guard"      # 护栏收口
    assert len(gw.trace) == 1                   # 只有成功的进入追踪
    print("✅ 全部通过: 模型网关（路由/护栏/成本/观测收口）")


if __name__ == "__main__":
    run()
