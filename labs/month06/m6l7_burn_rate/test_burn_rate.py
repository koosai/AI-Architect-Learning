# Month6 L7：错误预算燃尽率  （对应 docs/06-cloud-enterprise-industrial/observability-advanced.mdx）
# 目标：错误预算燃尽率分级告警——SRE 式“有意义告警”的核心
# 用法：python labs/month06/m6l7_burn_rate/test_burn_rate.py


def burn_rate(error_rate, budget):
    return error_rate / budget if budget else float("inf")


def alert_level(rate):
    if rate >= 14.4:
        return "page"        # 快烧：紧急寻呼
    if rate >= 6:
        return "page_slow"
    if rate >= 1:
        return "ticket"      # 慢烧：开工单
    return "ok"


def run():
    budget = 0.001           # 99.9% SLO -> 0.1% 错误预算
    assert alert_level(burn_rate(0.02, budget)) == "page"       # 燃尽率 20
    assert alert_level(burn_rate(0.007, budget)) == "page_slow"  # 7
    assert alert_level(burn_rate(0.002, budget)) == "ticket"     # 2
    assert alert_level(burn_rate(0.0005, budget)) == "ok"        # 0.5
    print("✅ 全部通过: 错误预算燃尽率分级告警")


if __name__ == "__main__":
    run()
