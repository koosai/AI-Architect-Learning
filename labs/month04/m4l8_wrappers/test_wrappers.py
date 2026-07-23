# Month4 L8：适配器 + 装饰器  （对应 docs/04-design-patterns-lld/adapter-decorator.mdx）
# 目标：包装+委托——适配器翻译接口、装饰器叠加功能，都不改原对象
# 用法：python labs/month04/m4l8_wrappers/test_wrappers.py


class OldPrinter:
    def print_upper(self, text):
        return text.upper()


class PrinterAdapter:
    # 适配器：把 OldPrinter 的旧接口翻译成统一的 render(text)
    def __init__(self, old):
        self.old = old

    def render(self, text):
        return self.old.print_upper(text)


def with_brackets(renderer):
    # 装饰器：包一层加功能，不改原对象
    def render(text):
        return "[" + renderer.render(text) + "]"
    return render


def run():
    adapter = PrinterAdapter(OldPrinter())
    assert adapter.render("hi") == "HI"          # 适配器翻译接口
    decorated = with_brackets(adapter)
    assert decorated("hi") == "[HI]"             # 装饰器叠加功能
    print("✅ 全部通过: 适配器翻译接口 / 装饰器叠加功能")


if __name__ == "__main__":
    run()
