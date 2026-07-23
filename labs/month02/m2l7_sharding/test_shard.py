# Month2 L7：分片  （对应 docs/02-system-design-bridge/scaling-strategies.mdx）
# 目标：看清朴素取模分片在扩容时几乎迁移所有 key，从而理解为何需要一致性哈希
# 用法：python labs/month02/m2l7_sharding/test_shard.py
import hashlib


def hash_int(key):
    return int(hashlib.md5(str(key).encode()).hexdigest(), 16)


def modulo_shard(key, n):
    return hash_int(key) % n


def remapped_fraction(n_from, n_to, keys):
    moved = sum(1 for k in keys if modulo_shard(k, n_from) != modulo_shard(k, n_to))
    return moved / len(keys)


def run():
    keys = [f"user{i}" for i in range(1000)]
    frac = remapped_fraction(4, 5, keys)   # 4 -> 5 个节点扩容
    assert frac > 0.5, frac                # 朴素取模通常迁移 ~80% 的 key
    assert remapped_fraction(4, 4, keys) == 0   # 节点数不变则零迁移
    print(f"✅ 全部通过: 朴素取模扩容迁移比例 ≈ {frac:.0%}（故需一致性哈希）")


if __name__ == "__main__":
    run()
