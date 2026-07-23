# Month7 L9：幻觉护栏  （对应 docs/07-llm-systems/hallucination-guardrails.mdx）
# 目标：答案必须有证据支撑 + 输出过滤——把不可靠输出收口
# 用法：python labs/month07/m7l9_guardrails/test_guardrails.py

BANNED = {"password", "secret_key"}


def guard(answer, context, citations):
    if not citations:
        return {"ok": False, "reason": "no_evidence"}       # 无证据
    for c in citations:
        if c not in context:
            return {"ok": False, "reason": "unsupported_citation"}   # 引用不在上下文里
    for w in BANNED:
        if w in answer:
            return {"ok": False, "reason": "filtered"}       # 敏感词过滤
    return {"ok": True, "answer": answer}


def run():
    ctx = "the sky is blue because of rayleigh scattering"
    assert guard("blue", ctx, ["rayleigh scattering"])["ok"] is True
    assert guard("blue", ctx, ["made up fact"])["reason"] == "unsupported_citation"
    assert guard("blue", ctx, [])["reason"] == "no_evidence"
    assert guard("your password is 123", ctx, ["rayleigh scattering"])["reason"] == "filtered"
    print("✅ 全部通过: 护栏（证据支撑 + 输出过滤）")


if __name__ == "__main__":
    run()
