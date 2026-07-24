# Month10 L11：多 Agent 评测与安全  （对应 docs/10-multi-agent-protocols/multi-agent-eval-safety.mdx）
# 目标：端到端+分步归因 和 系统级安全闸+人类监督——多 Agent 上生产的两道关
# 用法：python labs/month10/m10l11_eval_safety/test_eval_safety.py


def step_attribution(trace):
    for i, (name, ok) in enumerate(trace):
        if not ok:
            return {"failed_step": name, "index": i}   # 分步归因：定位第一个失败步
    return {"failed_step": None}


def safety_gate(action, risk):
    if risk == "high":
        return "require_human"        # 系统级安全闸 -> 人类监督
    return "proceed"


def run():
    trace = [("plan", True), ("search", True), ("write", False), ("review", True)]
    attr = step_attribution(trace)
    assert attr["failed_step"] == "write" and attr["index"] == 2
    assert safety_gate("deploy", "high") == "require_human"
    assert safety_gate("read", "low") == "proceed"
    print("✅ 全部通过: 分步归因 + 系统级安全闸+人类监督")


if __name__ == "__main__":
    run()
