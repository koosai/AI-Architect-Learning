# Month6 L5：基础设施即代码  （对应 docs/06-cloud-enterprise-industrial/infrastructure-as-code.mdx）
# 目标：期望 vs 状态 → diff → 幂等 apply——所有 IaC 工具的核心
# 用法：python labs/month06/m6l5_iac/test_iac.py


def plan(desired, current):
    actions = []
    for k, v in desired.items():
        if k not in current:
            actions.append(("create", k))
        elif current[k] != v:
            actions.append(("update", k))
    for k in current:
        if k not in desired:
            actions.append(("delete", k))
    return sorted(actions)


def apply(desired, current):
    for act, k in plan(desired, current):
        if act == "delete":
            current.pop(k, None)
        else:
            current[k] = desired[k]
    return current


def run():
    desired = {"vpc": "v1", "db": "pg14"}
    current = {"vpc": "v0"}
    assert plan(desired, current) == [("create", "db"), ("update", "vpc")]
    apply(desired, current)
    assert current == desired
    assert plan(desired, current) == []      # 幂等：再次 plan 无变化
    print("✅ 全部通过: IaC（期望vs状态→diff→幂等apply）")


if __name__ == "__main__":
    run()
