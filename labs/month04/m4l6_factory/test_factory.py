# Month4 L6：工厂 + 注册表  （对应 docs/04-design-patterns-lld/factory-pattern.mdx）
# 目标：集中创建 + 注册表——使用方面向接口，加类型不改工厂
# 用法：python labs/month04/m4l6_factory/test_factory.py

REGISTRY = {}


def register(kind):
    def deco(cls):
        REGISTRY[kind] = cls
        return cls
    return deco


@register("email")
class Email:
    def send(self, to):
        return f"email->{to}"


@register("sms")
class SMS:
    def send(self, to):
        return f"sms->{to}"


def create(kind):
    return REGISTRY[kind]()


def run():
    assert create("email").send("a") == "email->a"
    assert create("sms").send("b") == "sms->b"

    @register("push")   # 加类型 = 新增注册，create() 不改
    class Push:
        def send(self, to):
            return f"push->{to}"

    assert create("push").send("c") == "push->c"
    print("✅ 全部通过: 工厂+注册表（面向接口，加类型不改工厂）")


if __name__ == "__main__":
    run()
