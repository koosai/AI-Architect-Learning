# Month3 L7：缓存防穿透与防雪崩  （对应 docs/03-data-cache-queue/cache-problems.mdx）
# 目标：负缓存防穿透（不存在的 key 也缓存）；抖动 TTL 防雪崩（key 不同时过期）
# 用法：python labs/month03/m3l7_cache_guard/test_guard.py
import random

MISS = "__MISS__"


class GuardedCache:
    def __init__(self, db, base_ttl=10):
        self.db = db
        self.base_ttl = base_ttl
        self.store = {}

    def jitter_ttl(self, rng):
        return self.base_ttl + rng.randint(0, self.base_ttl)   # 加抖动，打散过期时刻

    def get(self, k):
        if k in self.store:
            return self.store[k]
        v = self.db.get(k, MISS)
        self.store[k] = v          # 命中或未命中都缓存（负缓存）
        return v


def run():
    db = {"a": 1}
    c = GuardedCache(db)
    assert c.get("a") == 1
    assert c.get("ghost") == MISS         # 不存在 -> 负缓存
    db.clear()                            # 模拟后端被清空
    assert c.get("ghost") == MISS         # 仍从负缓存返回，不再打库（防穿透）
    rng = random.Random(42)
    ttls = {c.jitter_ttl(rng) for _ in range(20)}
    assert len(ttls) > 1 and all(10 <= x <= 20 for x in ttls)  # TTL 分散（防雪崩）
    print("✅ 全部通过: 负缓存防穿透 / 抖动 TTL 防雪崩")


if __name__ == "__main__":
    run()
