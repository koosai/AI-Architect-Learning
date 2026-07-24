# Month12 L8：评估与可观测挂载  （对应 docs/12-capstone/eval-observability-build.mdx）
# 目标：把 trace 和评估集接进助手，让它可度量、可调试、可回归
# 用法：python labs/month12/m12l8_eval/test_eval.py


class AssistantWithEval:
    def __init__(self):
        self.traces = []

    def answer(self, q, fn):
        result = fn(q)
        self.traces.append({"q": q, "result": result})   # trace，可调试
        return result

    def run_eval(self, dataset, fn):
        correct = sum(1 for q, exp in dataset if fn(q) == exp)
        return correct / len(dataset)


def run():
    a = AssistantWithEval()
    a.answer("q1", lambda q: "a1")
    assert len(a.traces) == 1 and a.traces[0]["q"] == "q1"
    acc = a.run_eval([("q1", "a1"), ("q2", "a2")], lambda q: {"q1": "a1", "q2": "WRONG"}[q])
    assert acc == 0.5     # 可回归
    print("✅ 全部通过: 助手接 trace+评估集（可度量/可调试/可回归）")


if __name__ == "__main__":
    run()
