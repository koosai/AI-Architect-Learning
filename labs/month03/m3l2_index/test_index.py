# Month3 L2：复合索引最左前缀  （对应 docs/03-data-cache-queue/indexing.mdx）
# 目标：索引列顺序决定能加速哪些查询（最左前缀规则）
# 用法：python labs/month03/m3l2_index/test_index.py


def can_use_index(index_cols, query_cols):
    # 最左前缀：查询列必须是索引列的前缀，且顺序一致
    if len(query_cols) > len(index_cols):
        return False
    return list(index_cols[:len(query_cols)]) == list(query_cols)


def run():
    idx = ("user_id", "created_at")
    assert can_use_index(idx, ["user_id"]) is True
    assert can_use_index(idx, ["user_id", "created_at"]) is True
    assert can_use_index(idx, ["created_at"]) is False          # 跳过最左列 -> 用不上
    assert can_use_index(idx, ["created_at", "user_id"]) is False   # 顺序不符
    print("✅ 全部通过: 复合索引最左前缀规则")


if __name__ == "__main__":
    run()
