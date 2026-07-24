# Month9 L2：工具边界  （对应 docs/09-agent-architectures/tools-and-boundaries.mdx）
# 目标：schema + 权限 + 预算 + 审计——Agent 安全的第一道防线
# 用法：python labs/month09/m9l2_tools/test_tools.py


def make_tool(name, schema, requires_perm, cost):
    return {"name": name, "schema": schema, "perm": requires_perm, "cost": cost}


class ToolRunner:
    def __init__(self, tools, perms, budget):
        self.tools = {t["name"]: t for t in tools}
        self.perms = perms
        self.budget = budget
        self.audit = []

    def call(self, name, args):
        t = self.tools.get(name)
        if not t:
            return {"error": "unknown_tool"}
        for k in t["schema"]:                       # schema 校验
            if k not in args:
                return {"error": f"missing_arg:{k}"}
        if t["perm"] and t["perm"] not in self.perms:   # 权限
            return {"error": "no_permission"}
        if t["cost"] > self.budget:                 # 预算
            return {"error": "over_budget"}
        self.budget -= t["cost"]
        self.audit.append(name)                     # 审计
        return {"ok": name}


def run():
    tools = [make_tool("read", ["path"], None, 1), make_tool("delete", ["path"], "admin", 5)]
    r = ToolRunner(tools, perms=set(), budget=3)
    assert r.call("read", {"path": "/a"})["ok"] == "read"
    assert r.call("read", {})["error"] == "missing_arg:path"
    assert r.call("delete", {"path": "/a"})["error"] == "no_permission"
    r2 = ToolRunner(tools, perms={"admin"}, budget=3)
    assert r2.call("delete", {"path": "/a"})["error"] == "over_budget"
    assert r.audit == ["read"]
    print("✅ 全部通过: 工具（schema+权限+预算+审计）")


if __name__ == "__main__":
    run()
