# Month7 L6：结构化输出与工具调用  （对应 docs/07-llm-systems/structured-output-tools.mdx）
# 目标：校验 LLM 输出 + 安全地分发工具调用
# 用法：python labs/month07/m7l6_structured_tools/test_structured.py
import json


def validate_output(raw, required_keys):
    try:
        obj = json.loads(raw)
    except Exception:
        return None, "invalid_json"
    for k in required_keys:
        if k not in obj:
            return None, f"missing:{k}"
    return obj, None


ALLOWED_TOOLS = {"get_weather", "search"}


def dispatch(tool_call):
    name = tool_call.get("name")
    if name not in ALLOWED_TOOLS:
        return {"error": "tool_not_allowed"}     # 安全：白名单挡住越权工具
    return {"ok": name, "args": tool_call.get("args", {})}


def run():
    obj, err = validate_output('{"answer":"hi","score":1}', ["answer", "score"])
    assert err is None and obj["answer"] == "hi"
    _, err2 = validate_output("not json", ["a"])
    assert err2 == "invalid_json"
    _, err3 = validate_output('{"a":1}', ["a", "b"])
    assert err3 == "missing:b"
    assert dispatch({"name": "get_weather", "args": {"city": "SF"}})["ok"] == "get_weather"
    assert dispatch({"name": "rm_rf"}) == {"error": "tool_not_allowed"}
    print("✅ 全部通过: 校验 LLM 输出 + 工具调用白名单分发")


if __name__ == "__main__":
    run()
