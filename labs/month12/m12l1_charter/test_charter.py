# Month12 L1：立项文档  （对应 docs/12-capstone/capstone-kickoff.mdx）
# 目标：产出精悍、有边界、可验收的立项文档（后面所有阶段的北极星）
# 用法：python labs/month12/m12l1_charter/test_charter.py


def make_charter(problem, users, in_scope, out_scope, acceptance):
    return {"problem": problem, "users": users, "in_scope": in_scope,
            "out_scope": out_scope, "acceptance": acceptance}


def validate_charter(c):
    errors = []
    if not c["problem"]:
        errors.append("no_problem")
    if not c["in_scope"]:
        errors.append("no_scope")
    if not c["out_scope"]:
        errors.append("no_boundary")     # 必须写清不做什么
    if not c["acceptance"]:
        errors.append("no_acceptance")
    return errors


def run():
    c = make_charter("架构评审助手", "架构师", ["RAG问答", "评审"], ["不改代码"], ["能引用来源"])
    assert validate_charter(c) == []
    bad = make_charter("x", "y", ["z"], [], ["a"])
    assert "no_boundary" in validate_charter(bad)    # 缺边界被抓
    print("✅ 全部通过: 立项文档（问题/用户/边界/验收）")


if __name__ == "__main__":
    run()
