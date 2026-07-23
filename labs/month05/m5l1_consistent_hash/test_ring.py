# Month5 L1：一致性哈希  （对应 docs/05-core-components/load-balancing.mdx）
# 目标：环 + 顺时针归属 + 虚拟节点，验证扩缩容只迁移 ~1/N 的 key
# 用法：python labs/month05/m5l1_consistent_hash/test_ring.py
import hashlib
import bisect


class HashRing:
    def __init__(self, vnodes=100):
        self.vnodes = vnodes
        self.ring = []      # 有序的哈希点
        self.owner = {}     # 哈希点 -> 物理节点

    def _h(self, key):
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16)

    def add(self, node):
        for i in range(self.vnodes):
            h = self._h(f"{node}:{i}")
            bisect.insort(self.ring, h)
            self.owner[h] = node

    def get(self, key):
        if not self.ring:
            return None
        idx = bisect.bisect(self.ring, self._h(key)) % len(self.ring)   # 顺时针归属
        return self.owner[self.ring[idx]]


def run():
    r = HashRing(vnodes=100)
    for n in ["A", "B", "C", "D"]:
        r.add(n)
    keys = [f"k{i}" for i in range(2000)]
    before = {k: r.get(k) for k in keys}
    r.add("E")   # 4 -> 5 个节点扩容
    after = {k: r.get(k) for k in keys}
    frac = sum(1 for k in keys if before[k] != after[k]) / len(keys)
    assert 0.1 < frac < 0.35, frac   # 理论迁移 ~1/5=20%
    print(f"✅ 全部通过: 一致性哈希扩容只迁移 {frac:.0%}（~1/N）的 key")


if __name__ == "__main__":
    run()
