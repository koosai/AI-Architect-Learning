# Month7 L7：KV cache 与前缀缓存  （对应 docs/07-llm-systems/kv-cache-serving.mdx）
# 目标：用计算量模型量化 KV cache 和前缀缓存的收益
# 用法：python labs/month07/m7l7_kv_cache/test_kv_cache.py


def compute_no_cache(n):
    # 无 KV cache：生成第 i 个 token 要重算前 i 个 -> 1+2+...+n = O(n^2)
    return sum(range(1, n + 1))


def compute_with_cache(n):
    # 有 KV cache：每步只算增量 -> O(n)
    return n


def prefix_cache_saving(shared_prefix):
    # 前缀缓存：共享前缀无需重算
    return shared_prefix


def run():
    assert compute_no_cache(4) == 10 and compute_with_cache(4) == 4   # 省 6 单位算力
    assert compute_no_cache(100) > compute_with_cache(100)
    assert prefix_cache_saving(shared_prefix=100) == 100
    print("✅ 全部通过: KV cache 把 O(n^2) 降为 O(n) / 前缀缓存复用")


if __name__ == "__main__":
    run()
