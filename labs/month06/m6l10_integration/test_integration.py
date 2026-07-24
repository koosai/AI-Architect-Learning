# Month6 L10：企业系统集成  （对应 docs/06-cloud-enterprise-industrial/enterprise-erp-integration.mdx）
# 目标：按业务键幂等去重 + 主数据合并（golden record）
# 用法：python labs/month06/m6l10_integration/test_integration.py


class Integrator:
    def __init__(self):
        self.seen = set()
        self.master = {}

    def ingest(self, biz_key, record):
        if biz_key in self.seen:
            return "duplicate"                 # 业务键幂等去重
        self.seen.add(biz_key)
        m = self.master.setdefault(record["entity"], {})
        for k, v in record.items():
            if k != "entity" and (k not in m or not m[k]):
                m[k] = v                       # 主数据合并：多源字段补全
        return "merged"


def run():
    it = Integrator()
    assert it.ingest("evt1", {"entity": "cust1", "name": "Ada"}) == "merged"
    assert it.ingest("evt1", {"entity": "cust1", "name": "X"}) == "duplicate"   # 同事件去重
    it.ingest("evt2", {"entity": "cust1", "phone": "123"})                       # 补充字段
    assert it.master["cust1"] == {"name": "Ada", "phone": "123"}                 # 黄金记录
    print("✅ 全部通过: 企业集成（业务键幂等去重 + 主数据合并）")


if __name__ == "__main__":
    run()
