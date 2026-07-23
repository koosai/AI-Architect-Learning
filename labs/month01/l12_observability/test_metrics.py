# Lab L12：可观测性  （对应 docs/01-foundations/observability.mdx）
# 目标：原始日志 -> 可看趋势的指标（计数 / 错误率 / p50 / p95）
# 用法：python labs/month01/l12_observability/test_metrics.py


def _percentile(sorted_vals, p):
    if not sorted_vals:
        return 0
    k = int(round((p / 100) * (len(sorted_vals) - 1)))
    k = max(0, min(len(sorted_vals) - 1, k))
    return sorted_vals[k]


def aggregate(logs):
    # logs: [{"status": int, "latency_ms": float}, ...]
    n = len(logs)
    errors = sum(1 for e in logs if e["status"] >= 500)
    lats = sorted(e["latency_ms"] for e in logs)
    return {
        "count": n,
        "error_rate": errors / n if n else 0,
        "p50": _percentile(lats, 50),
        "p95": _percentile(lats, 95),
    }


def run():
    logs = [{"status": 200, "latency_ms": x} for x in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]]
    logs.append({"status": 500, "latency_ms": 200})
    m = aggregate(logs)
    assert m["count"] == 11, m
    assert abs(m["error_rate"] - 1 / 11) < 1e-9, m
    assert m["p50"] in (50, 60), m          # 中位数量级
    assert m["p95"] >= 100, m               # 尾部被 200ms 拉高
    print("✅ 全部通过: 日志聚合为 计数/错误率/p50/p95 指标")


if __name__ == "__main__":
    run()
