# Month9 L12：可靠 Agent 综合  （对应 docs/09-agent-architectures/capstone-agent.mdx）
# 目标：自主但受控、有边界、能停、可评测——把本月组件串成一个可靠 Agent
# 用法：python labs/month09/m9l12_agent/test_agent.py


class ReliableAgent:
    def __init__(self, perms, max_steps=5, budget=3):
        self.perms = perms
        self.max_steps = max_steps
        self.budget = budget
        self.audit = []

    def run_task(self, plan):
        # plan: [(tool, needs_perm, danger_level)]
        for i, (tool, perm, danger) in enumerate(plan):
            if i >= self.max_steps:
                return "stopped:max_steps"           # 能停
            if self.budget <= 0:
                return "stopped:budget"
            if perm and perm not in self.perms:
                return "blocked:permission"          # 有边界
            if danger >= 2:
                return "blocked:needs_approval"      # 受控
            self.budget -= 1
            self.audit.append(tool)
        return "done"


def run():
    assert ReliableAgent(set()).run_task([("read", None, 0), ("read", None, 0)]) == "done"
    assert ReliableAgent(set()).run_task([("delete", None, 2)]) == "blocked:needs_approval"
    assert ReliableAgent(set()).run_task([("write", "admin", 1)]) == "blocked:permission"
    assert ReliableAgent(set(), budget=1).run_task([("read", None, 0), ("read", None, 0)]) == "stopped:budget"
    print("✅ 全部通过: 可靠 Agent（自主但受控/有边界/能停/可评测）")


if __name__ == "__main__":
    run()
