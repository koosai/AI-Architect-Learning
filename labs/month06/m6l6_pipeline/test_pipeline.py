# Month6 L6：CI/CD 流水线  （对应 docs/06-cloud-enterprise-industrial/cicd-pipelines.mdx）
# 目标：阶段化 + 门禁 + fail-fast——所有 CI/CD 系统的骨架
# 用法：python labs/month06/m6l6_pipeline/test_pipeline.py


def run_pipeline(stages):
    executed = []
    for name, fn in stages:
        ok = fn()
        executed.append((name, ok))
        if not ok:
            return executed, False      # fail-fast：一阶段失败即中止
    return executed, True


def run():
    ok_stages = [("build", lambda: True), ("test", lambda: True), ("deploy", lambda: True)]
    ex, ok = run_pipeline(ok_stages)
    assert ok and len(ex) == 3
    bad_stages = [("build", lambda: True), ("test", lambda: False), ("deploy", lambda: True)]
    ex2, ok2 = run_pipeline(bad_stages)
    assert ok2 is False and [n for n, _ in ex2] == ["build", "test"]   # deploy 未执行
    print("✅ 全部通过: CI/CD 流水线（阶段化+门禁+fail-fast）")


if __name__ == "__main__":
    run()
