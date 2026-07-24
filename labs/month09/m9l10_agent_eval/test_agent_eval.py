# Month9 L10：Agent 评测  （对应 docs/09-agent-architectures/agent-evaluation.mdx）
# 目标：评整条轨迹的多维度指标——衡量和改进 Agent 的基础
# 用法：python labs/month09/m9l10_agent_eval/test_agent_eval.py


def eval_trajectory(traj, gold):
    return {
        "success": 1.0 if traj["goal_met"] else 0.0,
        "efficiency": gold["optimal_steps"] / traj["steps"] if traj["steps"] else 0,
        "reliability": 1.0 - traj["tool_errors"] / max(1, traj["steps"]),
    }


def run():
    m = eval_trajectory({"goal_met": True, "steps": 5, "tool_errors": 1}, {"optimal_steps": 4})
    assert m["success"] == 1.0
    assert abs(m["efficiency"] - 0.8) < 1e-9      # 4/5
    assert abs(m["reliability"] - 0.8) < 1e-9     # 1 - 1/5
    print("✅ 全部通过: Agent 轨迹多维评测（成功/效率/可靠）")


if __name__ == "__main__":
    run()
