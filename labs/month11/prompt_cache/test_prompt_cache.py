# Atlas · Claude / Gemini：前缀缓存  （对应 docs/atlas/claude-gemini.mdx）
# 目标：相同前缀（系统提示）复用，只算增量，省算力
# 用法：python labs/month11/prompt_cache/test_prompt_cache.py


class PrefixCache:
    def __init__(self):
        self.cache = {}

    def process(self, prefix, suffix):
        if prefix in self.cache:
            prefix_cost, hit = 0, True          # 前缀命中，不重算
        else:
            prefix_cost, hit = len(prefix), False
            self.cache[prefix] = True
        return {"cost": prefix_cost + len(suffix), "prefix_hit": hit}


def run():
    pc = PrefixCache()
    sys_prompt = "you are a helpful assistant"
    r1 = pc.process(sys_prompt, "q1")
    assert not r1["prefix_hit"]                       # 首次：算全部
    r2 = pc.process(sys_prompt, "q2")
    assert r2["prefix_hit"] and r2["cost"] == len("q2")   # 复用前缀，只算增量
    print("✅ 全部通过: 前缀缓存（相同系统提示复用，只算增量）")


if __name__ == "__main__":
    run()
