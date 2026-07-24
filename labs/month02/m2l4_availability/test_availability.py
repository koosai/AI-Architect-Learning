# Month2 L4：SLA/SLO/可用性  （对应 docs/02-system-design-bridge/sla-slo-availability.mdx）
# 目标：串联相乘 / 并联冗余 / 错误预算，都变成能算的数字
# 用法：python labs/month02/m2l4_availability/test_availability.py


def serial(components):
    # 串联依赖：可用性相乘（越串越低）
    r = 1.0
    for a in components:
        r *= a
    return r


def parallel(a, n):
    # n 个相同组件并联冗余：1 - (1-a)^n（越并越高）
    return 1 - (1 - a) ** n


def error_budget_minutes(availability, window_minutes=30 * 24 * 60):
    return (1 - availability) * window_minutes


def run():
    assert abs(serial([0.99, 0.99, 0.99]) - 0.970299) < 1e-6   # 三个串联 < 单个
    assert parallel(0.99, 2) > 0.99                            # 并联冗余高于单个组件
    assert abs(parallel(0.99, 2) - 0.9999) < 1e-9              # 双活：两个 2 个 9 -> 4 个 9
    assert abs(error_budget_minutes(0.999) - 43.2) < 0.1       # 99.9%/30天 ≈ 43.2 分钟
    print("✅ 全部通过: 串联相乘 / 并联冗余 / 错误预算")


if __name__ == "__main__":
    run()
