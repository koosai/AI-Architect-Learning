# Month12 L9：成本与性能挂载  （对应 docs/12-capstone/cost-performance-build.mdx）
# 目标：把路由/缓存/预算/归因挂到 provider 层，让助手付得起、够快
# 用法：python labs/month12/m12l9_cost/test_cost.py


class CostAwareProvider:
    def __init__(self, budget):
        self.budget = budget
        self.cache = {}
        self.by_feature = {}

    def complete(self, feature, prompt, difficulty=0.5):
        if prompt in self.cache:
            return {"result": self.cache[prompt], "source": "cache"}       # 缓存
        model = "big" if difficulty >= 0.7 else "small"                     # 路由
        cost = 5 if model == "big" else 1
        if sum(self.by_feature.values()) + cost > self.budget:
            return {"blocked": "budget"}                                    # 预算
        self.by_feature[feature] = self.by_feature.get(feature, 0) + cost   # 归因
        result = f"{model}:{prompt}"
        self.cache[prompt] = result
        return {"result": result, "model": model}


def run():
    p = CostAwareProvider(budget=6)
    assert p.complete("chat", "hi", difficulty=0.9)["model"] == "big"
    assert p.complete("chat", "hi")["source"] == "cache"          # 命中缓存
    assert p.complete("search", "q", difficulty=0.1)["model"] == "small"
    assert p.complete("search", "q2")["blocked"] == "budget"      # 超预算
    assert p.by_feature["chat"] == 5
    print("✅ 全部通过: provider 成本（路由/缓存/预算/归因）")


if __name__ == "__main__":
    run()
