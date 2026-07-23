# Lab L7：数据建模与索引  （对应 docs/01-foundations/data-modeling.mdx）
# 目标：先看查询、再设计结构；用索引把 O(n) 扫描变成 O(1) 命中
# 用法：python labs/month01/l7_modeling/test_index.py


def build_index(signups):
    idx = {}
    for s in signups:
        idx.setdefault(s["event"], []).append(s["user"])
    return idx


def users_of_event_scan(signups, event):
    return [s["user"] for s in signups if s["event"] == event]  # O(n) 全表扫描


def users_of_event_index(idx, event):
    return idx.get(event, [])  # O(1) 索引命中


def run():
    data = [
        {"user": "ada", "event": "e1"},
        {"user": "bob", "event": "e1"},
        {"user": "cy", "event": "e2"},
    ]
    idx = build_index(data)
    assert users_of_event_scan(data, "e1") == ["ada", "bob"]
    assert users_of_event_index(idx, "e1") == ["ada", "bob"]
    assert users_of_event_index(idx, "e2") == ["cy"]
    assert users_of_event_index(idx, "none") == []
    print("✅ 全部通过: 查询驱动建模，索引命中代替全表扫描")


if __name__ == "__main__":
    run()
