# Month10 L6：辩论与互审  （对应 docs/10-multi-agent-protocols/debate-review.mdx）
# 目标：独立批评 + 据评改进 + 收敛/上限——多 Agent 最不可替代的审查价值
# 用法：python labs/month10/m10l6_debate/test_debate.py


def debate(proposal, critic, improver, max_rounds=3):
    current = proposal
    history = [current]
    for _ in range(max_rounds):
        critique = critic(current)
        if critique is None:              # 收敛：无异议即停
            break
        current = improver(current, critique)   # 据评改进
        history.append(current)
    return current, history


def run():
    def critic(x):
        return None if len(x) >= 3 else "too short"

    def improver(x, c):
        return x + "x"

    final, hist = debate("a", critic, improver)
    assert final == "axx" and len(hist) == 3    # a -> ax -> axx 收敛
    print("✅ 全部通过: 辩论（独立批评+据评改进+收敛）")


if __name__ == "__main__":
    run()
