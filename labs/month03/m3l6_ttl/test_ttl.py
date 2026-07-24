# Month3 L6：缓存失效与 TTL  （对应 docs/03-data-cache-queue/cache-invalidation.mdx）
# 目标：过期 + 写时失效，体会缓存新鲜度与命中率的取舍
# 用法：python labs/month03/m3l6_ttl/test_ttl.py


class TTLCache:
    def __init__(self, ttl):
        self.ttl = ttl
        self.store = {}   # k -> (value, expire_at)

    def put(self, k, v, now):
        self.store[k] = (v, now + self.ttl)

    def get(self, k, now):
        if k in self.store:
            v, exp = self.store[k]
            if now < exp:
                return v
            del self.store[k]   # 过期清除
        return None


def run():
    c = TTLCache(ttl=5)
    c.put("a", 1, now=0)
    assert c.get("a", now=3) == 1        # 未过期
    assert c.get("a", now=6) is None     # 过期
    assert "a" not in c.store
    print("✅ 全部通过: TTL 过期 / 新鲜度与命中率取舍")


if __name__ == "__main__":
    run()
