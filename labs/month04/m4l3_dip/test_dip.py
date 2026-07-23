# Month4 L3：依赖倒置  （对应 docs/04-design-patterns-lld/solid-lsp-isp-dip.mdx）
# 目标：高层依赖抽象、具体实现注入——这是可测试、可替换架构的根
# 用法：python labs/month04/m4l3_dip/test_dip.py


class ReportService:
    def __init__(self, storage):
        self.storage = storage          # 依赖注入的抽象，不 new 具体类

    def save(self, name, data):
        return self.storage.write(name, data)


class MemoryStorage:
    def __init__(self):
        self.data = {}

    def write(self, name, data):
        self.data[name] = data
        return True


class FakeStorage:   # 测试替身
    def __init__(self):
        self.calls = []

    def write(self, name, data):
        self.calls.append(name)
        return True


def run():
    mem = MemoryStorage()
    svc = ReportService(mem)
    assert svc.save("r1", "x") is True and mem.data["r1"] == "x"

    fake = FakeStorage()             # 换实现无需改高层
    ReportService(fake).save("r2", "y")
    assert fake.calls == ["r2"]
    print("✅ 全部通过: DIP 依赖倒置（高层依赖抽象，实现可注入替换）")


if __name__ == "__main__":
    run()
