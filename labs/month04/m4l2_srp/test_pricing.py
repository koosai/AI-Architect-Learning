# Month4 L2：单一职责  （对应 docs/04-design-patterns-lld/solid-srp-ocp.mdx）
# 目标：每个函数只有一个变化的理由，且能独立测试
# 用法：python labs/month04/m4l2_srp/test_pricing.py


def subtotal(items):
    return sum(i["price"] * i["qty"] for i in items)


def discount(sub, rate):
    return sub * (1 - rate)


def with_tax(amount, tax):
    return round(amount * (1 + tax), 2)


def total(items, rate, tax):
    return with_tax(discount(subtotal(items), rate), tax)


def run():
    items = [{"price": 10, "qty": 2}, {"price": 5, "qty": 1}]  # 25
    assert subtotal(items) == 25          # 每个职责可独立测试
    assert discount(25, 0.2) == 20.0
    assert with_tax(20, 0.1) == 22.0
    assert total(items, 0.2, 0.1) == 22.0
    print("✅ 全部通过: SRP 单一职责（小计/折扣/税 各自独立可测）")


if __name__ == "__main__":
    run()
