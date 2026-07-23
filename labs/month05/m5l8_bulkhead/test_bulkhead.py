# Month5 L8：舱壁隔离  （对应 docs/05-core-components/bulkhead-isolation.mdx）
# 目标：每依赖独立并发上限 + 满则快速失败，故障被隔离在一个舱内
# 用法：python labs/month05/m5l8_bulkhead/test_bulkhead.py


class Bulkhead:
    def __init__(self, limits):
        self.limits = limits
        self.active = {k: 0 for k in limits}

    def acquire(self, dep):
        if self.active[dep] >= self.limits[dep]:
            return False               # 该舱满 -> 快速失败
        self.active[dep] += 1
        return True

    def release(self, dep):
        if self.active[dep] > 0:
            self.active[dep] -= 1


def run():
    b = Bulkhead({"db": 2, "cache": 1})
    assert b.acquire("db") and b.acquire("db")
    assert b.acquire("db") is False       # db 舱满
    assert b.acquire("cache") is True     # cache 舱不受影响（隔离）
    b.release("db")
    assert b.acquire("db") is True
    print("✅ 全部通过: 舱壁隔离（每依赖独立并发上限，故障隔离）")


if __name__ == "__main__":
    run()
