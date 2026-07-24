# Month5 L12：韧性服务综合  （对应 docs/05-core-components/capstone-resilient-service.mdx）
# 目标：把本月韧性构件组合成 resolve(code) 服务，在过载/依赖故障下提供有损服务
# 用法：python labs/month05/m5l12_resilient/test_resilient.py


class ResilientService:
    def __init__(self, backend):
        self.backend = backend
        self.cache = {}
        self.fails = 0
        self.open = False        # 断路器

    def resolve(self, code):
        if self.open:            # 断路器打开 -> 直接走降级
            return self.cache.get(code, "DEGRADED")
        try:
            v = self.backend(code)
            self.cache[code] = v      # 回填缓存
            self.fails = 0
            return v
        except Exception:
            self.fails += 1
            if self.fails >= 3:
                self.open = True      # 连续失败 -> 跳闸
            return self.cache.get(code, "DEGRADED")   # 有损服务


def run():
    state = {"fail": False}

    def backend(code):
        if state["fail"]:
            raise RuntimeError("down")
        return f"real:{code}"

    svc = ResilientService(backend)
    assert svc.resolve("x") == "real:x"     # 正常，并回填缓存
    state["fail"] = True
    for _ in range(3):
        svc.resolve("y")                    # 触发断路器
    assert svc.open is True
    assert svc.resolve("x") == "real:x"     # 降级：命中缓存返回旧值
    assert svc.resolve("z") == "DEGRADED"   # 无缓存 -> 有损占位
    print("✅ 全部通过: 韧性服务（断路 + 缓存降级，故障下有损可用）")


if __name__ == "__main__":
    run()
