# Month9 L1：Agent 核心循环  （对应 docs/09-agent-architectures/agent-loop-basics.mdx）
# 目标：观察-决策-行动-观察 + 停止条件——Agent 的核心骨架
# 用法：python labs/month09/m9l1_agent_loop/test_agent_loop.py


def agent_loop(state, policy, max_steps=10):
    trajectory = []
    for _ in range(max_steps):
        obs = state["obs"]
        action = policy(obs)                       # 决策
        trajectory.append((obs, action))
        if action == "stop":                       # 停止条件
            break
        state = state["transition"](state, action)  # 行动 -> 新观察
    return trajectory


def run():
    def policy(obs):
        return "stop" if obs >= 3 else "inc"

    def transition(s, a):
        return {"obs": s["obs"] + 1, "transition": s["transition"]}

    traj = agent_loop({"obs": 0, "transition": transition}, policy)
    assert [a for _, a in traj] == ["inc", "inc", "inc", "stop"]
    print("✅ 全部通过: Agent 循环（观察-决策-行动 + 停止条件）")


if __name__ == "__main__":
    run()
