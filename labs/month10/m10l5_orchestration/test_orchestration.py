# Month10 L5：顺序与并行编排  （对应 docs/10-multi-agent-protocols/sequential-parallel.mdx）
# 目标：流水线 + 扇出聚合 + 容错——按依赖编排多 Agent
# 用法：python labs/month10/m10l5_orchestration/test_orchestration.py


def pipeline(stages, x):
    for s in stages:
        x = s(x)                  # 顺序流水线
    return x


def fanout_aggregate(workers, x, aggregate):
    results = [w(x) for w in workers]     # 扇出
    return aggregate(results)             # 聚合


def fault_tolerant(workers, x):
    out = []
    for w in workers:
        try:
            out.append(w(x))
        except Exception:
            out.append(None)      # 容错：单个失败不影响整体
    return out


def run():
    assert pipeline([lambda v: v + 1, lambda v: v * 2], 3) == 8
    assert fanout_aggregate([lambda v: v, lambda v: v * 10], 2, sum) == 22

    def bad(v):
        raise RuntimeError()

    assert fault_tolerant([lambda v: v, bad, lambda v: v + 1], 5) == [5, None, 6]
    print("✅ 全部通过: 编排（流水线+扇出聚合+容错）")


if __name__ == "__main__":
    run()
