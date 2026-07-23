# Month9 L3：ReAct 模式  （对应 docs/09-agent-architectures/react-pattern.mdx）
# 目标：推理-行动-观察交织，体会推理如何引导行动、轨迹如何便于排错
# 用法：python labs/month09/m9l3_react/test_react.py


def react(question, tools, max_steps=5):
    trace = []
    observations = []
    for _ in range(max_steps):
        if not observations:                     # Reason
            thought, action = "need weather", ("get_weather", "SF")
        else:
            thought, action = "have data, finish", ("finish", None)
        obs = tools[action[0]](action[1]) if action[0] in tools else None   # Act + Observe
        if obs is not None:
            observations.append(obs)
        trace.append((thought, action[0], obs))
        if action[0] == "finish":
            break
    return trace


def run():
    tools = {"get_weather": lambda c: "20C", "finish": lambda _: None}
    trace = react("weather in SF?", tools)
    kinds = [a for _, a, _ in trace]
    assert "get_weather" in kinds and kinds[-1] == "finish"
    assert ("need weather", "get_weather", "20C") in trace   # 观察被记录，便于排错
    print("✅ 全部通过: ReAct（推理-行动-观察交织，轨迹可排错）")


if __name__ == "__main__":
    run()
