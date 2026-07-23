# Month10 L3：Supervisor 编排  （对应 docs/10-multi-agent-protocols/supervisor-orchestration.mdx）
# 目标：分配-收集-决策-出口——多 Agent 最可控的协作骨架
# 用法：python labs/month10/m10l3_supervisor/test_supervisor.py


class Supervisor:
    def __init__(self, workers):
        self.workers = workers        # {name: fn}

    def run(self, assignment):
        results = {}
        for worker, subtask in assignment.items():
            results[worker] = self.workers[worker](subtask)          # 分配 + 收集
        decision = max(results.values(), key=lambda r: r["score"])   # 决策
        return {"outputs": results, "final": decision["answer"]}      # 出口


def run():
    workers = {"a": lambda t: {"answer": "A", "score": 3}, "b": lambda t: {"answer": "B", "score": 5}}
    s = Supervisor(workers)
    out = s.run({"a": "sub1", "b": "sub2"})
    assert out["final"] == "B" and len(out["outputs"]) == 2   # b 得分高被选
    print("✅ 全部通过: Supervisor（分配-收集-决策-出口）")


if __name__ == "__main__":
    run()
