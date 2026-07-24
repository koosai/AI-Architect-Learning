# Month11 L10：可靠性与容量  （对应 docs/11-production-ai-platform/reliability-capacity.mdx）
# 目标：重试 + 多模型 failover + 降级——单个模型抖动不砸给用户
# 用法：python labs/month11/m11l10_reliability/test_reliability.py


def call_with_reliability(models, request, max_retries=2):
    # models: [(name, fn)]，按优先级；每个先重试，再 failover 到下一个
    for name, fn in models:
        for attempt in range(max_retries):
            try:
                return {"model": name, "result": fn(request), "attempts": attempt + 1}
            except Exception:
                continue
    return {"model": None, "result": "DEGRADED"}     # 全部失败 -> 降级


def run():
    calls = {"n": 0}

    def flaky(r):
        calls["n"] += 1
        if calls["n"] < 2:
            raise RuntimeError()
        return "ok"

    r = call_with_reliability([("primary", flaky)], "req")
    assert r["result"] == "ok" and r["attempts"] == 2    # 重试成功

    def dead(r):
        raise RuntimeError()

    r2 = call_with_reliability([("primary", dead), ("backup", lambda r: "backup_ok")], "req")
    assert r2["model"] == "backup"                        # failover 到备用模型
    r3 = call_with_reliability([("p", dead)], "req")
    assert r3["result"] == "DEGRADED"                     # 全挂 -> 降级
    print("✅ 全部通过: 可靠性（重试+多模型failover+降级）")


if __name__ == "__main__":
    run()
