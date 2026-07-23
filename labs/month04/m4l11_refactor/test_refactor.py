# Month4 L11：坏味道重构  （对应 docs/04-design-patterns-lld/code-smells-refactoring.mdx）
# 目标：测试护体 -> 识别坏味道 -> 小步重构 -> 行为不变
# 用法：python labs/month04/m4l11_refactor/test_refactor.py


def price_before(t, qty):
    # 坏味道：魔法数字 + 重复分支
    if t == "vip":
        return qty * 100 * 0.8
    elif t == "normal":
        return qty * 100 * 1.0
    else:
        return qty * 100


UNIT = 100
DISCOUNT = {"vip": 0.8, "normal": 1.0}


def price_after(t, qty):
    # 重构：表驱动，消除魔法数字与重复
    return qty * UNIT * DISCOUNT.get(t, 1.0)


def run():
    # 测试护体：重构前后对所有输入行为必须完全一致
    for t in ["vip", "normal", "guest"]:
        for q in [1, 3, 10]:
            assert price_before(t, q) == price_after(t, q), (t, q)
    print("✅ 全部通过: 重构到表驱动，行为完全不变")


if __name__ == "__main__":
    run()
