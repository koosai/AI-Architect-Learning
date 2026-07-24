# Month10 L9：Agent 协议  （对应 docs/10-multi-agent-protocols/agent-protocols.mdx）
# 目标：统一接口让工具即插即用 + 权限边界，体会协议的互操作价值
# 用法：python labs/month10/m10l9_protocol/test_protocol.py


class Tool:
    def __init__(self, name, handler, scope):
        self.name = name
        self.handler = handler
        self.scope = scope


class Host:
    def __init__(self, granted_scopes):
        self.tools = {}
        self.granted = granted_scopes

    def register(self, tool):
        self.tools[tool.name] = tool          # 即插即用，无需为每个工具定制

    def invoke(self, name, args):
        t = self.tools.get(name)
        if not t:
            return {"error": "not_found"}
        if t.scope not in self.granted:
            return {"error": "scope_denied"}  # 权限边界
        return {"result": t.handler(args)}


def run():
    host = Host(granted_scopes={"read"})
    host.register(Tool("get", lambda a: f"got {a}", "read"))
    host.register(Tool("rm", lambda a: "deleted", "write"))
    assert host.invoke("get", "file")["result"] == "got file"    # 统一接口即插即用
    assert host.invoke("rm", "file")["error"] == "scope_denied"   # 权限边界
    print("✅ 全部通过: 协议（统一接口即插即用+权限边界）")


if __name__ == "__main__":
    run()
