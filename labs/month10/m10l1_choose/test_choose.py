# Month10 L1：是否该用多 Agent  （对应 docs/10-multi-agent-protocols/why-multi-agent.mdx）
# 目标：按任务性质选最简方案——抵制滥用多 Agent 的判断力
# 用法：python labs/month10/m10l1_choose/test_choose.py


def choose(task):
    if task.get("subtasks", 1) <= 1:
        return "single_agent"
    if task.get("independent_perspectives") or task.get("parallel_specialties"):
        return "multi_agent"     # 需要独立视角/并行专精 -> 才用多 Agent
    return "single_agent"


def run():
    assert choose({"subtasks": 1}) == "single_agent"
    assert choose({"subtasks": 3, "parallel_specialties": True}) == "multi_agent"
    assert choose({"subtasks": 3, "independent_perspectives": True}) == "multi_agent"
    assert choose({"subtasks": 3}) == "single_agent"   # 多子任务但无需分工 -> 仍单 Agent
    print("✅ 全部通过: 抵制滥用多 Agent（按任务性质选最简）")


if __name__ == "__main__":
    run()
