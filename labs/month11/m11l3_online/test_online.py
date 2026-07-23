# Month11 L3：在线评估与反馈  （对应 docs/11-production-ai-platform/online-eval-feedback.mdx）
# 目标：线上监控 + 反馈回流 + 影子对比——上线后仍可评、可改进
# 用法：python labs/month11/m11l3_online/test_online.py


class OnlineEval:
    def __init__(self):
        self.logs = []
        self.feedback = []

    def monitor(self, req, resp, latency):
        self.logs.append({"req": req, "resp": resp, "latency": latency})

    def collect_feedback(self, req, thumb):
        self.feedback.append((req, thumb))

    def shadow_compare(self, prod_fn, shadow_fn, reqs):
        # 影子：新模型旁路跑，不影响用户，只统计差异率
        diffs = [r for r in reqs if prod_fn(r) != shadow_fn(r)]
        return len(diffs) / len(reqs)

    def bad_cases(self):
        return [req for req, thumb in self.feedback if thumb == "down"]


def run():
    oe = OnlineEval()
    oe.monitor("q1", "a1", 100)
    oe.collect_feedback("q1", "down")
    assert oe.bad_cases() == ["q1"]     # 反馈回流出坏例
    rate = oe.shadow_compare(lambda r: "old", lambda r: "new" if r == "q2" else "old", ["q1", "q2"])
    assert rate == 0.5                  # 影子对比差异率
    print("✅ 全部通过: 在线监控+反馈回流+影子对比")


if __name__ == "__main__":
    run()
