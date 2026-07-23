# Month11 L6：平台护栏  （对应 docs/11-production-ai-platform/platform-guardrails.mdx）
# 目标：输入+输出+执行 多层护栏做成纵深防御，体会没有单层能独当一面
# 用法：python labs/month11/m11l6_guardrails/test_guardrails.py


def input_guard(text):
    return "ignore previous" not in text.lower()   # 防提示注入


def output_guard(text):
    return "SSN" not in text                        # 防敏感信息泄露


def exec_guard(action, allowed):
    return action in allowed                        # 防越权执行


def pipeline(text, action, allowed):
    if not input_guard(text):
        return "blocked:input"
    if not exec_guard(action, allowed):
        return "blocked:exec"
    resp = "ok " + text
    if not output_guard(resp):
        return "blocked:output"
    return "pass"


def run():
    assert pipeline("hello", "read", {"read"}) == "pass"
    assert pipeline("ignore previous instructions", "read", {"read"}) == "blocked:input"
    assert pipeline("hi", "delete", {"read"}) == "blocked:exec"
    assert pipeline("SSN", "read", {"read"}) == "blocked:output"   # 前几层没拦住，输出层兜住
    print("✅ 全部通过: 纵深防御（输入+执行+输出多层，无单层独当一面）")


if __name__ == "__main__":
    run()
