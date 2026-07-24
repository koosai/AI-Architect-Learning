# Month12 L12：作品集陈述  （对应 docs/12-capstone/showcase-and-path.mdx）
# 目标：把作品浓缩成一页有判断力的架构陈述，并准备好应对追问
# 用法：python labs/month12/m12l12_pitch/test_pitch.py


def build_pitch(problem, approach, key_decisions, tradeoffs):
    return {"problem": problem, "approach": approach,
            "key_decisions": key_decisions, "tradeoffs": tradeoffs}


def answer_challenge(pitch, question):
    for d in pitch["key_decisions"] + pitch["tradeoffs"]:
        if any(w in d for w in question.split()):
            return d                       # 用决策/取舍应对追问
    return "需进一步分析"


def validate_pitch(p):
    # 有判断力 = 必须包含取舍与关键决策，不能只罗列功能
    return len(p["tradeoffs"]) > 0 and len(p["key_decisions"]) > 0


def run():
    p = build_pitch("架构评审慢", "RAG+Agent 助手",
                    ["用 pgvector 做检索"], ["选最终一致换取低运维成本"])
    assert validate_pitch(p)
    assert not validate_pitch(build_pitch("x", "y", [], []))   # 只罗列功能 -> 不合格
    assert "pgvector" in answer_challenge(p, "为什么用 pgvector")
    print("✅ 全部通过: 架构陈述（有判断力: 决策+取舍，能应对追问）")


if __name__ == "__main__":
    run()
