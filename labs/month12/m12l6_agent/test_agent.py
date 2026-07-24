# Month12 L6：评审 Agent 核心用例  （对应 docs/12-capstone/agent-tools-build.mdx）
# 目标：一个该用 Agent、且克制地用（只读边界+停止条件）的评审助手
# 用法：python labs/month12/m12l6_agent/test_agent.py


class ReviewAssistant:
    READ_ONLY = {"read_file", "list_files", "grep"}

    def __init__(self, max_steps=5):
        self.max_steps = max_steps
        self.actions = []

    def act(self, tool, arg):
        if len(self.actions) >= self.max_steps:
            return "stopped:max_steps"                # 停止条件
        if tool not in self.READ_ONLY:
            return "blocked:not_readonly"             # 只读边界（克制）
        self.actions.append((tool, arg))
        return f"ok:{tool}"


def run():
    a = ReviewAssistant(max_steps=3)
    assert a.act("read_file", "x.py") == "ok:read_file"
    assert a.act("write_file", "x.py") == "blocked:not_readonly"
    a.act("grep", "foo")
    a.act("list_files", ".")
    assert a.act("read_file", "y") == "stopped:max_steps"
    print("✅ 全部通过: 评审助手（该用 agent + 克制：只读边界+停止）")


if __name__ == "__main__":
    run()
