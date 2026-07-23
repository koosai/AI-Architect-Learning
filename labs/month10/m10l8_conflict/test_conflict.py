# Month10 L8：冲突与共识  （对应 docs/10-multi-agent-protocols/conflict-consensus.mdx）
# 目标：多个冲突意见 -> 一个结论，层次化收敛（投票 -> 加权 -> 仲裁 -> 暴露）
# 用法：python labs/month10/m10l8_conflict/test_conflict.py
from collections import Counter


def resolve(opinions, weights=None):
    if weights is None:
        c = Counter(opinions)
        top, cnt = c.most_common(1)[0]
        if list(c.values()).count(cnt) == 1:
            return {"method": "vote", "result": top}          # 多数票
        return {"method": "expose", "result": "tie", "options": sorted(c)}   # 平票 -> 暴露
    scores = {}
    for op, w in zip(opinions, weights):
        scores[op] = scores.get(op, 0) + w
    return {"method": "weighted", "result": max(scores, key=scores.get)}     # 加权仲裁


def run():
    r1 = resolve(["A", "A", "B"])
    assert r1["method"] == "vote" and r1["result"] == "A"
    r2 = resolve(["A", "B"])
    assert r2["method"] == "expose" and r2["result"] == "tie"       # 平票暴露
    r3 = resolve(["A", "B"], weights=[1, 5])
    assert r3["method"] == "weighted" and r3["result"] == "B"
    print("✅ 全部通过: 冲突收敛（投票->加权->仲裁->暴露）")


if __name__ == "__main__":
    run()
