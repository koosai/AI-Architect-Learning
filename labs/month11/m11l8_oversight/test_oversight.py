# Month11 L8：人类监督与降级  （对应 docs/11-production-ai-platform/human-oversight-fallback.mdx）
# 目标：出错/没把握/高风险/不可用时怎么办——把它做成一等决策逻辑
# 用法：python labs/month11/m11l8_oversight/test_oversight.py


def decide(confidence, risk, model_available):
    if not model_available:
        return "fallback:cached_or_static"   # 模型不可用
    if risk == "high":
        return "human_review"                # 高风险
    if confidence < 0.5:
        return "ask_clarification"           # 没把握
    return "auto"


def run():
    assert decide(0.9, "low", True) == "auto"
    assert decide(0.3, "low", True) == "ask_clarification"
    assert decide(0.9, "high", True) == "human_review"
    assert decide(0.9, "low", False) == "fallback:cached_or_static"
    print("✅ 全部通过: 人类监督/降级（管理失败而非假装不失败）")


if __name__ == "__main__":
    run()
