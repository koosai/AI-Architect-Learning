# Month4 L4：组合优于继承  （对应 docs/04-design-patterns-lld/composition-over-inheritance.mdx）
# 目标：组合可替换的行为部件，比继承更灵活、且能运行时替换
# 用法：python labs/month04/m4l4_composition/test_duck.py


class Duck:
    def __init__(self, fly, quack):
        self.fly = fly       # 行为部件通过组合注入
        self.quack = quack

    def do_fly(self):
        return self.fly()

    def do_quack(self):
        return self.quack()


def run():
    d = Duck(fly=lambda: "flap", quack=lambda: "quack")
    assert d.do_fly() == "flap" and d.do_quack() == "quack"
    d.fly = lambda: "rocket"          # 运行时替换飞行行为（继承做不到）
    assert d.do_fly() == "rocket"
    rubber = Duck(fly=lambda: "can't fly", quack=lambda: "squeak")
    assert rubber.do_quack() == "squeak"
    print("✅ 全部通过: 组合优于继承（行为可插拔、可运行时替换）")


if __name__ == "__main__":
    run()
