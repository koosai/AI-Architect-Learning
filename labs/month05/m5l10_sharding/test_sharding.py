# Month5 L10：固定分片平滑再平衡  （对应 docs/05-core-components/partitioning-sharding.mdx）
# 目标：固定 partition + 节点映射 + 平滑再平衡，验证扩容只搬一小部分
# 用法：python labs/month05/m5l10_sharding/test_sharding.py
import hashlib


class ShardMap:
    def __init__(self, num_partitions, nodes):
        self.p = num_partitions
        self.nodes = list(nodes)
        self.assign = [self.nodes[i % len(self.nodes)] for i in range(self.p)]

    def _h(self, key):
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16)

    def partition_of(self, key):
        return self._h(key) % self.p       # key->partition 固定，永不变

    def node_of(self, key):
        return self.assign[self.partition_of(key)]

    def add_node(self, node):
        self.nodes.append(node)
        moved = 0
        for i in range(self.p):            # 只把少量 partition 迁到新节点
            if i % len(self.nodes) == len(self.nodes) - 1:
                self.assign[i] = node
                moved += 1
        return moved


def run():
    sm = ShardMap(num_partitions=12, nodes=["A", "B", "C"])
    keys = [f"k{i}" for i in range(500)]
    before = {k: sm.node_of(k) for k in keys}
    moved_parts = sm.add_node("D")
    after = {k: sm.node_of(k) for k in keys}
    moved_frac = sum(1 for k in keys if before[k] != after[k]) / len(keys)
    assert moved_parts > 0 and moved_frac < 0.5, (moved_parts, moved_frac)   # 只搬一小部分
    print(f"✅ 全部通过: 固定分片扩容只迁移 {moved_frac:.0%} 的 key（key->partition 不变）")


if __name__ == "__main__":
    run()
