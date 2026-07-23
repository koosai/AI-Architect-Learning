# Month5 L4：反向代理/CDN 边缘缓存  （对应 docs/05-core-components/reverse-proxy-cdn.mdx）
# 目标：命中 / 回源 / TTL / purge，体会 CDN 怎么降延迟、护源站
# 用法：python labs/month05/m5l4_edge_cache/test_edge.py


class EdgeCache:
    def __init__(self, origin, ttl=10):
        self.origin = origin
        self.ttl = ttl
        self.store = {}
        self.origin_hits = 0

    def get(self, key, now):
        if key in self.store:
            v, exp = self.store[key]
            if now < exp:
                return v                 # 命中，不回源
        v = self.origin(key)             # 回源
        self.origin_hits += 1
        self.store[key] = (v, now + self.ttl)
        return v

    def purge(self, key):
        self.store.pop(key, None)


def run():
    origin = lambda k: f"page:{k}"
    c = EdgeCache(origin, ttl=10)
    assert c.get("/a", now=0) == "page:/a" and c.origin_hits == 1    # miss 回源
    assert c.get("/a", now=5) == "page:/a" and c.origin_hits == 1    # 命中，护源站
    assert c.get("/a", now=20) == "page:/a" and c.origin_hits == 2   # 过期回源
    c.purge("/a")
    assert c.get("/a", now=21) == "page:/a" and c.origin_hits == 3   # purge 后回源
    print("✅ 全部通过: 边缘缓存（命中/回源/TTL/purge，护源站）")


if __name__ == "__main__":
    run()
