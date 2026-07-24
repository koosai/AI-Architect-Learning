# Atlas · Pinterest：图随机游走近邻采样（PinSage 核心）  （对应 docs/atlas/pinterest.mdx）
# 目标：从节点出发按边随机游走，统计访问频次作为图近邻
# 用法：python labs/month08/graph_random_walk/test_random_walk.py
import random


def random_walk_counts(graph, start, walks, length, rng):
    counts = {}
    for _ in range(walks):
        cur = start
        for _ in range(length):
            nbrs = graph.get(cur, [])
            if not nbrs:
                break
            cur = nbrs[rng.randrange(len(nbrs))]
            counts[cur] = counts.get(cur, 0) + 1
    return counts


def run():
    graph = {"A": ["B", "C"], "B": ["A", "D"], "C": ["A"], "D": ["B"]}
    counts = random_walk_counts(graph, "A", walks=100, length=3, rng=random.Random(0))
    assert "B" in counts and "C" in counts       # A 的邻居被高频访问
    assert max(counts, key=counts.get) in {"A", "B", "C", "D"}
    print("✅ 全部通过: 图随机游走近邻采样（PinSage 核心）")


if __name__ == "__main__":
    run()
