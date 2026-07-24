# Month7 L2：token 预算拼装  （对应 docs/07-llm-systems/tokenization-context.mdx）
# 目标：估 token + 按优先级在预算内拼装上下文
# 用法：python labs/month07/m7l2_token_budget/test_budget.py


def est_tokens(text):
    return len(text.split())          # 简化：按词数估 token


def assemble(parts, budget):
    # parts: [(priority, text)]，优先级数字小的先放
    used = 0
    chosen = []
    for prio, text in sorted(parts, key=lambda x: x[0]):
        t = est_tokens(text)
        if used + t <= budget:
            chosen.append(text)
            used += t
    return chosen, used


def run():
    parts = [
        (1, "system prompt here"),          # 3 token，最高优先
        (3, "old chat history long text"),  # 5 token，最低优先
        (2, "user question now"),           # 3 token
    ]
    chosen, used = assemble(parts, budget=6)
    assert "system prompt here" in chosen
    assert "user question now" in chosen
    assert "old chat history long text" not in chosen   # 预算不够，低优先被裁
    assert used <= 6
    print("✅ 全部通过: token 预算内按优先级拼装上下文")


if __name__ == "__main__":
    run()
