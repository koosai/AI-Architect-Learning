# Month7 L5：成本与延迟估算  （对应 docs/07-llm-systems/llm-api-cost-latency.mdx）
# 目标：按 token×档位算成本、按输出算延迟、按难度路由模型
# 用法：python labs/month07/m7l5_cost_latency/test_cost.py

PRICE = {"small": (0.5, 1.5), "large": (5, 15)}   # (输入 $/1k, 输出 $/1k)


def cost(model, in_tok, out_tok):
    pi, po = PRICE[model]
    return round(in_tok / 1000 * pi + out_tok / 1000 * po, 4)


def latency_ms(out_tok, ms_per_tok=10):
    return out_tok * ms_per_tok          # 延迟主要由输出 token 数决定


def route(difficulty):
    return "large" if difficulty >= 0.7 else "small"   # 难任务才上大模型


def run():
    assert cost("small", 1000, 500) == 1.25    # 0.5 + 0.75
    assert cost("large", 1000, 500) == 12.5    # 5 + 7.5
    assert latency_ms(200) == 2000
    assert route(0.9) == "large" and route(0.3) == "small"
    print("✅ 全部通过: 成本(token×档位)/延迟(按输出)/难度路由")


if __name__ == "__main__":
    run()
