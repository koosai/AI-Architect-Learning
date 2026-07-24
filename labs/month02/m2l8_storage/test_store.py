# Month2 L8：存储选型  （对应 docs/02-system-design-bridge/storage-selection.mdx）
# 目标：按访问模式选存储，告别“默认就用 MySQL”
# 用法：python labs/month02/m2l8_storage/test_store.py


def choose_storage(access):
    if access.get("pattern") == "key_lookup" and access.get("latency") == "sub_ms":
        return "redis"          # 纯 KV、亚毫秒
    if access.get("pattern") == "analytics" and access.get("scan") == "columnar":
        return "clickhouse"     # 列存 OLAP、大范围聚合
    if access.get("pattern") == "full_text":
        return "elasticsearch"  # 全文检索
    if access.get("consistency") == "transactional":
        return "postgres"       # 强事务
    return "postgres"           # 合理默认


def run():
    assert choose_storage({"pattern": "key_lookup", "latency": "sub_ms"}) == "redis"
    assert choose_storage({"pattern": "analytics", "scan": "columnar"}) == "clickhouse"
    assert choose_storage({"pattern": "full_text"}) == "elasticsearch"
    assert choose_storage({"consistency": "transactional"}) == "postgres"
    assert choose_storage({}) == "postgres"
    print("✅ 全部通过: 按访问模式选存储")


if __name__ == "__main__":
    run()
