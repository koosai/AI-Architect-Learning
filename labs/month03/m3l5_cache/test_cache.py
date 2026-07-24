# Month3 L5：缓存模式  （对应 docs/03-data-cache-queue/cache-patterns.mdx）
# 目标：读时回填（read-through）+ 写时失效 + 命中统计
# 用法：python labs/month03/m3l5_cache/test_cache.py


class Cache:
    def __init__(self, db):
        self.db = db
        self.store = {}
        self.hits = 0
        self.misses = 0

    def get(self, k):
        if k in self.store:
            self.hits += 1
            return self.store[k]
        self.misses += 1
        v = self.db.get(k)          # 回源
        if v is not None:
            self.store[k] = v       # 回填
        return v

    def write(self, k, v):
        self.db[k] = v
        self.store.pop(k, None)     # 写时失效


def run():
    db = {"a": 1}
    c = Cache(db)
    assert c.get("a") == 1 and c.misses == 1     # miss -> 回填
    assert c.get("a") == 1 and c.hits == 1       # hit
    c.write("a", 2)                              # 失效
    assert "a" not in c.store
    assert c.get("a") == 2 and c.misses == 2     # 重新回填新值
    print("✅ 全部通过: 读时回填 / 写时失效 / 命中统计")


if __name__ == "__main__":
    run()
