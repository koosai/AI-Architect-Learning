# Atlas · Bing + Copilot：Prometheus 编排  （对应 docs/atlas/bing-copilot.mdx）
# 目标：决定是否需要搜索，grounding 后再生成——传统搜索接入 LLM 的编排层
# 用法：python labs/month08/prometheus_control_loop/test_prometheus.py


def orchestrate(query, has_fresh_need):
    steps = []
    if has_fresh_need:
        steps.append("search")     # 需时效信息 -> 先搜索
        steps.append("ground")     # 用搜索结果做 grounding
    steps.append("generate")
    return steps


def run():
    assert orchestrate("今天天气", has_fresh_need=True) == ["search", "ground", "generate"]
    assert orchestrate("1+1=?", has_fresh_need=False) == ["generate"]   # 无需搜索
    print("✅ 全部通过: Prometheus 编排（按需搜索+grounding+生成）")


if __name__ == "__main__":
    run()
