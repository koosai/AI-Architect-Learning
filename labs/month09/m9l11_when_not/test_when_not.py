# Month9 L11：何时不该用 Agent  （对应 docs/09-agent-architectures/when-not-agent.mdx）
# 目标：按任务性质选最简方案——抵制过度用 Agent 的判断力
# 用法：python labs/month09/m9l11_when_not/test_when_not.py


def choose(task):
    if task.get("deterministic") and task.get("fixed_steps"):
        return "script"          # 确定流程 -> 脚本，别上 Agent
    if task.get("single_call"):
        return "single_llm"      # 一次调用够 -> 单次 LLM
    if task.get("needs_tools") and task.get("multi_step"):
        return "agent"           # 多步 + 工具 -> 才用 Agent
    return "single_llm"          # 默认最简


def run():
    assert choose({"deterministic": True, "fixed_steps": True}) == "script"
    assert choose({"single_call": True}) == "single_llm"
    assert choose({"needs_tools": True, "multi_step": True}) == "agent"
    assert choose({}) == "single_llm"
    print("✅ 全部通过: 抵制过度用 Agent（按任务性质选最简方案）")


if __name__ == "__main__":
    run()
