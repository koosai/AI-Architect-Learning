# Month10 L7：交接路由  （对应 docs/10-multi-agent-protocols/handoff-routing.mdx）
# 目标：按能力把请求分派给对的专精 Agent + 兜底——可控的中心化路由
# 用法：python labs/month10/m10l7_routing/test_routing.py

ROUTES = {"code": "engineer", "legal": "lawyer", "math": "mathematician"}


def route(intent, agents):
    target = ROUTES.get(intent)
    if target and target in agents:
        return target
    return "generalist"          # 无对应专精 -> 兜底


def run():
    agents = {"engineer", "lawyer", "generalist"}
    assert route("code", agents) == "engineer"
    assert route("legal", agents) == "lawyer"
    assert route("math", agents) == "generalist"      # 无 mathematician -> 兜底
    assert route("unknown", agents) == "generalist"
    print("✅ 全部通过: 中心化路由（按能力分派+兜底）")


if __name__ == "__main__":
    run()
