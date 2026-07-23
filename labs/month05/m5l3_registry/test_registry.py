# Month5 L3：服务发现注册中心  （对应 docs/05-core-components/service-discovery.mdx）
# 目标：注册 + 心跳续约 + TTL 摘除 + 查询健康实例
# 用法：python labs/month05/m5l3_registry/test_registry.py


class Registry:
    def __init__(self, ttl=10):
        self.ttl = ttl
        self.instances = {}    # id -> (addr, expire_at)

    def register(self, iid, addr, now):
        self.instances[iid] = (addr, now + self.ttl)

    def heartbeat(self, iid, now):
        if iid in self.instances:
            addr, _ = self.instances[iid]
            self.instances[iid] = (addr, now + self.ttl)   # 续约

    def healthy(self, now):
        return sorted(iid for iid, (_, exp) in self.instances.items() if now < exp)


def run():
    r = Registry(ttl=10)
    r.register("i1", "10.0.0.1", now=0)
    r.register("i2", "10.0.0.2", now=0)
    assert r.healthy(now=5) == ["i1", "i2"]
    r.heartbeat("i1", now=8)              # 只有 i1 续约
    assert r.healthy(now=12) == ["i1"]    # i2 过期被摘除
    print("✅ 全部通过: 服务发现（注册/心跳续约/TTL摘除/查健康实例）")


if __name__ == "__main__":
    run()
