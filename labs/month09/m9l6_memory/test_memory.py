# Month9 L6：工作记忆  （对应 docs/09-agent-architectures/agent-memory.mdx）
# 目标：目标 + 进度 + 发现 + 防重复——Agent 多步连贯的工作记忆
# 用法：python labs/month09/m9l6_memory/test_memory.py


class WorkingMemory:
    def __init__(self, goal):
        self.goal = goal
        self.progress = []
        self.findings = []
        self.done_actions = set()

    def record_action(self, action):
        if action in self.done_actions:
            return False                     # 防重复：做过的不再做
        self.done_actions.add(action)
        self.progress.append(action)
        return True

    def add_finding(self, f):
        self.findings.append(f)

    def summary(self):
        return {"goal": self.goal, "steps": len(self.progress), "findings": self.findings}


def run():
    m = WorkingMemory("find bug")
    assert m.record_action("read log") is True
    assert m.record_action("read log") is False    # 已做过
    m.add_finding("null pointer at L10")
    s = m.summary()
    assert s["goal"] == "find bug" and s["steps"] == 1 and "null pointer at L10" in s["findings"]
    print("✅ 全部通过: 工作记忆（目标+进度+发现+防重复）")


if __name__ == "__main__":
    run()
