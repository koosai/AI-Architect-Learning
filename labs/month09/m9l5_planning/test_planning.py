# Month9 L5：规划与分解  （对应 docs/09-agent-architectures/planning-decomposition.mdx）
# 目标：分解 + 按计划执行 + 计划修正——复杂多步任务的骨架
# 用法：python labs/month09/m9l5_planning/test_planning.py


def make_plan(goal):
    return {"cook": ["buy", "prep", "cook", "serve"]}.get(goal, [goal])


def execute_plan(plan, fail_at=None):
    done = []
    for task in plan:
        if task == fail_at:
            done.append("retry_" + task)     # 计划修正：先补救再执行
        done.append(task)
    return done


def run():
    plan = make_plan("cook")
    assert plan == ["buy", "prep", "cook", "serve"]
    assert execute_plan(plan) == plan
    done2 = execute_plan(["buy", "prep"], fail_at="prep")
    assert "retry_prep" in done2 and done2.index("retry_prep") < done2.index("prep")
    print("✅ 全部通过: 规划（分解+执行+计划修正）")


if __name__ == "__main__":
    run()
