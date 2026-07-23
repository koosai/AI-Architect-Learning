# Month11 L4：AI 可观测性  （对应 docs/11-production-ai-platform/ai-observability.mdx）
# 目标：把一次 AI 请求变成可追踪、可归因的链路——质量/成本/延迟每步可见
# 用法：python labs/month11/m11l4_observability/test_observability.py


class Trace:
    def __init__(self, trace_id):
        self.trace_id = trace_id
        self.spans = []

    def span(self, name, cost=0, latency=0, quality=None):
        self.spans.append({"name": name, "cost": cost, "latency": latency, "quality": quality})

    def total_cost(self):
        return sum(s["cost"] for s in self.spans)

    def total_latency(self):
        return sum(s["latency"] for s in self.spans)

    def slowest(self):
        return max(self.spans, key=lambda s: s["latency"])["name"]


def run():
    t = Trace("req-1")
    t.span("retrieve", cost=0.001, latency=50)
    t.span("generate", cost=0.02, latency=800)
    assert round(t.total_cost(), 3) == 0.021
    assert t.total_latency() == 850
    assert t.slowest() == "generate"     # 归因：最慢的一步
    print("✅ 全部通过: AI 请求链路可追踪可归因（质量/成本/延迟）")


if __name__ == "__main__":
    run()
