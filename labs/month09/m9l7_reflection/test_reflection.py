# Month9 L7：反思与纠错  （对应 docs/09-agent-architectures/reflection-correction.mdx）
# 目标：检查-诊断-调整-重试——让 Agent 能自我纠错而非一错到底
# 用法：python labs/month09/m9l7_reflection/test_reflection.py


def solve_with_reflection(task, attempt_fn, check_fn, max_tries=3):
    feedback = None
    for i in range(max_tries):
        result = attempt_fn(task, feedback)     # 调整：用上次反馈
        ok, diag = check_fn(result)             # 检查 + 诊断
        if ok:
            return result, i + 1
        feedback = diag                          # 反馈驱动下次重试
    return None, max_tries


def run():
    def attempt(task, feedback):
        return "42" if feedback == "need number" else "abc"

    def check(r):
        return (r.isdigit(), "need number")

    result, tries = solve_with_reflection("q", attempt, check)
    assert result == "42" and tries == 2         # 第 2 次用反馈修正成功
    print("✅ 全部通过: 反思（检查-诊断-调整-重试）")


if __name__ == "__main__":
    run()
