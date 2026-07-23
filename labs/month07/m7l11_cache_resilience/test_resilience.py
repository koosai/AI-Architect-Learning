# Month7 L11：LLM 缓存与韧性  （对应 docs/07-llm-systems/llm-caching-resilience.mdx）
# 目标：语义缓存 + 模型降级链 + 成本上限
# 用法：python labs/month07/m7l11_cache_resilience/test_resilience.py


class LLMResilience:
    def __init__(self, budget):
        self.cache = {}
        self.spent = 0
        self.budget = budget

    def _norm(self, q):
        return q.lower().strip().rstrip("?")     # 归一化 -> 相似问命中同一缓存

    def ask(self, q, models):
        key = self._norm(q)
        if key in self.cache:
            return self.cache[key], "cache"      # 语义缓存命中
        for name, fn, price in models:           # 降级链：依次尝试
            if self.spent + price > self.budget:
                continue                          # 超预算跳过贵模型
            try:
                ans = fn(q)
                self.spent += price
                self.cache[key] = ans
                return ans, name
            except Exception:
                continue                          # 该模型失败 -> 降级到下一个
        return None, "exhausted"


def run():
    big = ("big", lambda q: "big_ans", 10)
    small = ("small", lambda q: "small_ans", 1)
    r = LLMResilience(budget=5)
    ans, src = r.ask("Hello?", [big, small])     # big 超预算(10>5) -> 降级 small
    assert ans == "small_ans" and src == "small"
    ans2, src2 = r.ask("hello", [big, small])    # 归一化后命中语义缓存
    assert ans2 == "small_ans" and src2 == "cache"
    print("✅ 全部通过: 语义缓存 + 降级链 + 成本上限")


if __name__ == "__main__":
    run()
