# Month12 L2：架构决策  （对应 docs/12-capstone/architecture-decisions.mdx）
# 目标：立项转成组件图 + 数据流 + 关键 ADR，让架构可评审、经得起追问
# 用法：python labs/month12/m12l2_adr/test_adr.py


def make_adr(title, context, decision, consequences):
    return {"title": title, "context": context, "decision": decision, "consequences": consequences}


def validate_adr(adr):
    return all(adr.get(k) for k in ["title", "context", "decision", "consequences"])


def architecture_valid(components, data_flows):
    names = {c["name"] for c in components}
    for src, dst in data_flows:
        if src not in names or dst not in names:
            return False                 # 数据流引用了不存在的组件
    return True


def run():
    adr = make_adr("用向量检索", "需语义匹配", "选 pgvector", "运维简单但规模有限")
    assert validate_adr(adr)
    assert not validate_adr({"title": "x"})       # 不完整
    comps = [{"name": "gateway"}, {"name": "retriever"}, {"name": "llm"}]
    assert architecture_valid(comps, [("gateway", "retriever"), ("retriever", "llm")])
    assert not architecture_valid(comps, [("gateway", "ghost")])
    print("✅ 全部通过: 架构决策（组件图+数据流+ADR）")


if __name__ == "__main__":
    run()
