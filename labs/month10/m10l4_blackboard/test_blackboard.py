# Month10 L4：黑板共享状态  （对应 docs/10-multi-agent-protocols/communication-state.mdx）
# 目标：结构化共享状态 + 防污染——多 Agent 可靠通信的基础
# 用法：python labs/month10/m10l4_blackboard/test_blackboard.py


class Blackboard:
    def __init__(self, schema):
        self.schema = schema      # {key: type}
        self.data = {}

    def write(self, agent, key, value):
        if key not in self.schema:
            return "rejected:unknown_key"     # 防污染：只允许约定的 key
        if not isinstance(value, self.schema[key]):
            return "rejected:bad_type"        # 类型校验
        self.data[key] = {"by": agent, "value": value}
        return "ok"

    def read(self, key):
        return self.data.get(key, {}).get("value")


def run():
    bb = Blackboard(schema={"finding": str, "count": int})
    assert bb.write("a1", "finding", "bug found") == "ok"
    assert bb.write("a2", "count", 5) == "ok"
    assert bb.write("a3", "random", "x") == "rejected:unknown_key"
    assert bb.write("a4", "count", "not int") == "rejected:bad_type"
    assert bb.read("finding") == "bug found"
    print("✅ 全部通过: 黑板（结构化共享状态+防污染）")


if __name__ == "__main__":
    run()
