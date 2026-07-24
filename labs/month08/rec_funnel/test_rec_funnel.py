# Atlas · YouTube 推荐：两阶段漏斗  （对应 docs/atlas/youtube-recommendation.mdx）
# 目标：召回（海量->候选）+ 排序（候选->精排）的两阶段推荐
# 用法：python labs/month08/rec_funnel/test_rec_funnel.py


def recall(all_items, user_interests, limit):
    scored = [(i, len(set(i["tags"]) & set(user_interests))) for i in all_items]
    return [i for i, s in sorted(scored, key=lambda x: -x[1]) if s > 0][:limit]


def rank(candidates, watch_time_model):
    return sorted(candidates, key=lambda i: -watch_time_model(i))   # 按预估观看时长精排


def run():
    items = [{"id": 1, "tags": ["cat"]}, {"id": 2, "tags": ["dog"]}, {"id": 3, "tags": ["cat", "cute"]}]
    cand = recall(items, ["cat"], limit=10)
    ids = {i["id"] for i in cand}
    assert ids == {1, 3} and 2 not in ids        # 召回：兴趣相关
    ranked = rank(cand, lambda i: i["id"])
    assert ranked[0]["id"] == 3
    print("✅ 全部通过: 两阶段推荐漏斗（召回+排序）")


if __name__ == "__main__":
    run()
