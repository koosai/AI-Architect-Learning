# Month7 L1：自回归生成  （对应 docs/07-llm-systems/transformer-autoregression.mdx）
# 目标：预测下一个 token → 追加 → 再预测 的核心循环
# 用法：python labs/month07/m7l1_autoregress/test_autoregress.py

NEXT = {"the": "cat", "cat": "sat", "sat": "down", "down": "<eos>"}


def generate(start, max_tokens=10):
    out = [start]
    cur = start
    for _ in range(max_tokens):
        nxt = NEXT.get(cur, "<eos>")
        if nxt == "<eos>":
            break
        out.append(nxt)      # 追加生成的 token
        cur = nxt            # 再以它为输入，预测下一个
    return out


def run():
    assert generate("the") == ["the", "cat", "sat", "down"]
    assert generate("cat") == ["cat", "sat", "down"]
    assert generate("unknown") == ["unknown"]   # 无后继直接停
    print("✅ 全部通过: 自回归生成（预测→追加→再预测）")


if __name__ == "__main__":
    run()
