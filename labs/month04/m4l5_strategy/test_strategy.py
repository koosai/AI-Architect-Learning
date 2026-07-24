# Month4 L5：策略模式  （对应 docs/04-design-patterns-lld/strategy-pattern.mdx）
# 目标：一族可互换算法 + context 委托——加新算法时 context 一行不改
# 用法：python labs/month04/m4l5_strategy/test_strategy.py


class Checkout:
    def __init__(self, strategy):
        self.strategy = strategy       # 注入的算法

    def pay(self, amount):
        return self.strategy(amount)   # context 只委托，不关心具体算法


def alipay(a):
    return f"alipay:{a}"


def card(a):
    return f"card:{a}"


def run():
    assert Checkout(alipay).pay(100) == "alipay:100"
    assert Checkout(card).pay(50) == "card:50"

    def crypto(a):                     # 加新算法，Checkout 一行不改
        return f"btc:{a}"

    assert Checkout(crypto).pay(10) == "btc:10"
    print("✅ 全部通过: 策略模式（算法互换，context 不改）")


if __name__ == "__main__":
    run()
