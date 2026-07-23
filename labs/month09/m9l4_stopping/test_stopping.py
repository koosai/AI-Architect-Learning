# Month9 L4：停止与预算  （对应 docs/09-agent-architectures/stopping-budget.mdx）
# 目标：最大步数 + 循环检测 + 预算——Agent 必备的安全带
# 用法：python labs/month09/m9l4_stopping/test_stopping.py


class SafetyBelt:
    def __init__(self, max_steps, budget):
        self.max_steps = max_steps
        self.budget = budget
        self.steps = 0
        self.history = []

    def check(self, action):
        self.steps += 1
        if self.steps > self.max_steps:
            return "stop:max_steps"
        if self.budget <= 0:
            return "stop:budget"
        if self.history[-2:] == [action, action]:     # 连续第 3 次同动作 = 空转
            return "stop:loop"
        self.history.append(action)
        self.budget -= 1
        return "continue"


def run():
    sb = SafetyBelt(max_steps=10, budget=5)
    assert sb.check("a") == "continue"
    assert sb.check("a") == "continue"
    assert sb.check("a") == "stop:loop"          # 循环检测

    sb2 = SafetyBelt(max_steps=2, budget=100)
    sb2.check("x")
    sb2.check("y")
    assert sb2.check("z") == "stop:max_steps"

    sb3 = SafetyBelt(max_steps=100, budget=1)
    sb3.check("x")
    assert sb3.check("y") == "stop:budget"
    print("✅ 全部通过: 安全带（最大步数+循环检测+预算）")


if __name__ == "__main__":
    run()
