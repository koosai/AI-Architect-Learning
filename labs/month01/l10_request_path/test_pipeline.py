# Lab L10：请求路径  （对应 docs/01-foundations/request-path.mdx）
# 目标：关键路径耗时=串行相加；缓存命中省掉下游；扇出并行=取最慢
# 用法：python labs/month01/l10_request_path/test_pipeline.py


def path_latency(stages, cache_hit=False, cached_stage=None, cached_cost=1):
    total = 0
    for name, cost in stages:
        if cache_hit and name == cached_stage:
            total += cached_cost   # 命中缓存：用极小代价取代原耗时
        else:
            total += cost
    return total


def fanout_latency(parallel_calls):
    return max(parallel_calls)     # 并行扇出：端到端 = 最慢的那个


def run():
    stages = [("auth", 5), ("db", 50), ("render", 5)]
    assert path_latency(stages) == 60
    assert path_latency(stages, cache_hit=True, cached_stage="db", cached_cost=2) == 12
    assert fanout_latency([30, 50, 10]) == 50
    print("✅ 全部通过: 关键路径串行相加 / 缓存命中 / 扇出取最大")


if __name__ == "__main__":
    run()
