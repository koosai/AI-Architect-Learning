# Month9 L9：Agent 护栏  （对应 docs/09-agent-architectures/agent-guardrails.mdx）
# 目标：危险动作分级 + 人在回路审批 + 最小信任
# 用法：python labs/month09/m9l9_guardrails/test_guardrails.py

DANGER = {"read": 0, "write": 1, "delete": 2, "deploy": 2}


def classify(action):
    return DANGER.get(action, 1)     # 未知动作按中危处理（最小信任）


def gate(action, approvals):
    level = classify(action)
    if level == 0:
        return "auto"                # 只读 -> 自动放行
    if level >= 2 and "human" not in approvals:
        return "needs_approval"      # 高危 -> 人在回路
    return "allow"


def run():
    assert gate("read", set()) == "auto"
    assert gate("write", set()) == "allow"
    assert gate("delete", set()) == "needs_approval"
    assert gate("delete", {"human"}) == "allow"
    assert gate("unknown_action", set()) == "allow"   # 未知按中危，不自动
    print("✅ 全部通过: 护栏（危险分级+人在回路+最小信任）")


if __name__ == "__main__":
    run()
