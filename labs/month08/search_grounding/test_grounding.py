# Atlas · Gemini：搜索 grounding  （对应 docs/atlas/gemini.mdx）
# 目标：用检索证据约束生成；无证据则声明不确定，不编造
# 用法：python labs/month08/search_grounding/test_grounding.py


def grounded_answer(question, evidence):
    if not evidence:
        return {"answer": "我不确定", "grounded": False}
    return {"answer": f"{evidence[0]}（来源已核实）", "grounded": True, "cite": evidence[0]}


def run():
    r = grounded_answer("首都", ["巴黎是法国首都"])
    assert r["grounded"] and "巴黎" in r["answer"]
    r2 = grounded_answer("未知问题", [])
    assert not r2["grounded"] and "不确定" in r2["answer"]   # 无证据不编造
    print("✅ 全部通过: 搜索 grounding（有证据才答）")


if __name__ == "__main__":
    run()
