# Month3 L11：事务性 Outbox  （对应 docs/03-data-cache-queue/consistency-patterns.mdx）
# 目标：本地事务原子写入 业务数据 + 事件；中继器可靠投递（最终一致）
# 用法：python labs/month03/m3l11_outbox/test_outbox.py


class OutboxSystem:
    def __init__(self):
        self.orders = {}
        self.outbox = []
        self.published = []

    def create_order(self, oid, data):
        # 同一“本地事务”：写订单 + 写 outbox 事件，原子（要么都成、要么都不）
        self.orders[oid] = data
        self.outbox.append({"event": "order_created", "oid": oid, "sent": False})

    def relay(self):
        # 中继器扫描未发送事件，投递后标记；可重复运行且不重复投递
        for e in self.outbox:
            if not e["sent"]:
                self.published.append(e["oid"])
                e["sent"] = True


def run():
    s = OutboxSystem()
    s.create_order(1, {"amt": 100})
    assert 1 in s.orders and len(s.outbox) == 1
    s.relay()
    assert s.published == [1]
    s.relay()                       # 再次中继不重复投递
    assert s.published == [1]
    print("✅ 全部通过: 事务性 outbox + 可靠中继（最终一致）")


if __name__ == "__main__":
    run()
