# Month11 L9：成本工程  （对应 docs/11-production-ai-platform/cost-engineering.mdx）
# 目标：归因 + 路由降本 + 预算防失控——让 AI 成本可预测可控
# 用法：python labs/month11/m11l9_cost/test_cost.py


class CostManager:
    def __init__(self, budget):
        self.budget = budget
        self.by_feature = {}

    def route(self, difficulty):
        return "cheap" if difficulty < 0.7 else "expensive"   # 路由降本

    def charge(self, feature, cost):
        if sum(self.by_feature.values()) + cost > self.budget:
            return "over_budget"                              # 预算防失控
        self.by_feature[feature] = self.by_feature.get(feature, 0) + cost   # 成本归因
        return "ok"


def run():
    cm = CostManager(budget=10)
    assert cm.route(0.3) == "cheap" and cm.route(0.9) == "expensive"
    assert cm.charge("search", 4) == "ok"
    assert cm.charge("chat", 4) == "ok"
    assert cm.charge("chat", 5) == "over_budget"
    assert cm.by_feature["search"] == 4
    print("✅ 全部通过: 成本工程（归因+路由降本+预算防失控）")


if __name__ == "__main__":
    run()
