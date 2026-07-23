# Month10 L10：多 Agent 运维  （对应 docs/10-multi-agent-protocols/multi-agent-ops.mdx）
# 目标：可观测(追踪) + 成本控制(全局预算) + 错误隔离(校验防传染) 做进一个运行器
# 用法：python labs/month10/m10l10_ops/test_ops.py


class OpsRunner:
    def __init__(self, budget):
        self.budget = budget
        self.trace = []
        self.spent = 0

    def run(self, steps):
        # steps: [(name, fn, cost, validator)]
        for name, fn, cost, validator in steps:
            if self.spent + cost > self.budget:
                self.trace.append((name, "skipped:budget"))     # 全局预算
                continue
            out = fn()
            if not validator(out):
                self.trace.append((name, "quarantined"))        # 错误隔离：不向下传染
                continue
            self.spent += cost
            self.trace.append((name, "ok"))                     # 可观测追踪
        return self.trace


def run():
    r = OpsRunner(budget=10)
    steps = [
        ("a", lambda: "good", 3, lambda o: o == "good"),
        ("b", lambda: "bad", 3, lambda o: o == "good"),   # 校验失败 -> 隔离
        ("c", lambda: "good", 3, lambda o: o == "good"),
    ]
    trace = r.run(steps)
    assert ("a", "ok") in trace and ("b", "quarantined") in trace and ("c", "ok") in trace
    assert r.spent == 6      # b 未计费
    print("✅ 全部通过: 多 Agent 运维（追踪+全局预算+错误隔离）")


if __name__ == "__main__":
    run()
