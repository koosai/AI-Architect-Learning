# Lab L8：并发与乐观锁  （对应 docs/01-foundations/concurrency-basics.mdx）
# 目标：理解“先读后写”的竞态，再用版本号(CAS)乐观并发控制根治超卖
# 用法：python labs/month01/l8_concurrency/test_seats.py


class Inventory:
    def __init__(self, stock):
        self.stock = stock
        self.version = 0

    def reserve_cas(self, expected_version):
        # 乐观锁：库存充足且版本匹配才扣减并递增版本；否则失败，让调用方带新版本重试
        if self.stock > 0 and self.version == expected_version:
            self.stock -= 1
            self.version += 1
            return True
        return False


def run():
    inv = Inventory(1)
    v = inv.version
    # 模拟两个并发请求都读到了同一个旧版本 v
    assert inv.reserve_cas(v) is True    # A 先提交，成功
    assert inv.reserve_cas(v) is False   # B 用过期版本 v 提交 -> 冲突，阻止超卖
    assert inv.stock == 0, inv.stock
    # 拿到新版本后可以继续（此例已无库存）
    assert inv.reserve_cas(inv.version) is False
    print("✅ 全部通过: 乐观并发控制(CAS)阻止超卖")


if __name__ == "__main__":
    run()
