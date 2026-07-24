# Month10 L2：角色专精  （对应 docs/10-multi-agent-protocols/roles-specialization.mdx）
# 目标：每个角色单一职责 + 最小工具权限——多 Agent 专精和安全的基础
# 用法：python labs/month10/m10l2_roles/test_roles.py

ROLES = {
    "researcher": {"tools": {"search", "read"}},
    "writer": {"tools": {"write"}},
    "reviewer": {"tools": {"read"}},
}


def can_use(role, tool):
    return tool in ROLES.get(role, {}).get("tools", set())


def run():
    assert can_use("researcher", "search") and can_use("researcher", "read")
    assert not can_use("researcher", "write")     # 研究员无写权限（最小权限）
    assert can_use("writer", "write") and not can_use("writer", "search")
    assert not can_use("reviewer", "write")        # 审查者只读
    print("✅ 全部通过: 角色专精（单一职责+最小工具权限）")


if __name__ == "__main__":
    run()
