# Month7 L12：端到端 LLM 应用  （对应 docs/07-llm-systems/capstone-llm-app.mdx）
# 目标：把本月组件串成端到端功能——可靠性来自包裹模型的工程
# 用法：python labs/month07/m7l12_llm_app/test_llm_app.py
import json


class LLMApp:
    def __init__(self):
        self.cache = {}

    def answer(self, question, context):
        if question in self.cache:
            return self.cache[question]          # 缓存
        # mock 模型：从 context 找答案，并声明引用
        if "blue" in context:
            raw = '{"answer":"blue","cited":"blue"}'
        else:
            raw = '{"answer":"unknown","cited":""}'
        obj = json.loads(raw)                     # 结构化输出校验
        if not obj["cited"] or obj["cited"] not in context:
            result = {"ok": False, "reason": "no_evidence"}   # 护栏
        else:
            result = {"ok": True, "answer": obj["answer"]}
        self.cache[question] = result
        return result


def run():
    app = LLMApp()
    r = app.answer("what color", "the sky is blue")
    assert r["ok"] and r["answer"] == "blue"
    r3 = app.answer("other q", "no relevant info")
    assert r3["ok"] is False and r3["reason"] == "no_evidence"   # 无证据被护栏拦
    print("✅ 全部通过: 端到端 LLM 应用（拼装/提示/校验/护栏/缓存）")


if __name__ == "__main__":
    run()
