# Lab L15：性能与延迟  （对应 docs/01-foundations/performance-and-latency.mdx）
# 目标：用百分位看性能；定位瓶颈阶段
# 用法：python labs/month01/l15_performance/test_perf.py


def percentile(data, p):
    if not data:
        return 0
    s = sorted(data)
    k = int(round((p / 100) * (len(s) - 1)))
    k = max(0, min(len(s) - 1, k))
    return s[k]


def bottleneck(stage_latencies):
    # 返回耗时最大的阶段名
    return max(stage_latencies, key=stage_latencies.get)


def run():
    lat = list(range(1, 101))  # 1..100
    assert percentile(lat, 50) in (50, 51), percentile(lat, 50)
    assert percentile(lat, 99) in (99, 100), percentile(lat, 99)
    assert percentile(lat, 100) == 100
    assert bottleneck({"auth": 5, "db": 80, "render": 15}) == "db"
    print("✅ 全部通过: 百分位统计 / 瓶颈定位")


if __name__ == "__main__":
    run()
