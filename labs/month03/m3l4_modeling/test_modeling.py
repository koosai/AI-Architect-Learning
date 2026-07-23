# Month3 L4：SQL 规范化 vs NoSQL 反规范化  （对应 docs/03-data-cache-queue/sql-vs-nosql.mdx）
# 目标：亲手体会规范化 join 与反规范化嵌入的等价与取舍
# 用法：python labs/month03/m3l4_modeling/test_modeling.py


def normalized_query(users, orders, order_id):
    # 规范化：两表 join（无冗余，但读要连接）
    o = next(o for o in orders if o["id"] == order_id)
    u = next(u for u in users if u["id"] == o["user_id"])
    return {"order": order_id, "user_name": u["name"]}


def denormalized_query(orders_embedded, order_id):
    # 反规范化：user_name 冗余嵌入订单（读一次搞定，代价是冗余与一致性维护）
    o = next(o for o in orders_embedded if o["id"] == order_id)
    return {"order": order_id, "user_name": o["user_name"]}


def run():
    users = [{"id": 1, "name": "Ada"}]
    orders = [{"id": 100, "user_id": 1}]
    orders_embedded = [{"id": 100, "user_id": 1, "user_name": "Ada"}]
    a = normalized_query(users, orders, 100)
    b = denormalized_query(orders_embedded, 100)
    assert a == b == {"order": 100, "user_name": "Ada"}, (a, b)  # 结果等价
    print("✅ 全部通过: 规范化 join 与反规范化嵌入等价（取舍：读性能 vs 冗余/一致性）")


if __name__ == "__main__":
    run()
