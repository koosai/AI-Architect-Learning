# Lab L13：测试先行 (TDD)  （对应 docs/01-foundations/testing-and-tdd.mdx）
# 目标：先让测试定义正确（尤其边界），再让实现满足；Money.allocate 不丢一分钱
# 用法：python labs/month01/l13_testing/test_money.py


class Money:
    def __init__(self, cents):
        self.cents = int(cents)

    def __eq__(self, o):
        return isinstance(o, Money) and o.cents == self.cents

    def __repr__(self):
        return f"Money({self.cents})"

    def add(self, o):
        return Money(self.cents + o.cents)

    def allocate(self, n):
        # 尽量平均分成 n 份，余数从前往后每份补 1 分，保证总和不变
        base, rem = divmod(self.cents, n)
        return [Money(base + (1 if i < rem else 0)) for i in range(n)]


def run():
    assert Money(100).add(Money(50)) == Money(150)
    parts = Money(100).allocate(3)  # 100 分成 3 份：34,33,33
    assert [p.cents for p in parts] == [34, 33, 33], parts
    assert sum(p.cents for p in parts) == 100, "一分都不能丢"
    assert [p.cents for p in Money(5).allocate(2)] == [3, 2]
    print("✅ 全部通过: TDD 下的 Money.allocate 不丢分")


if __name__ == "__main__":
    run()
