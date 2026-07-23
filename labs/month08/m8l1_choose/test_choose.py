# Month8 L1：知识方案选型  （对应 docs/08-rag/why-rag.mdx）
# 目标：按知识性质选 prompt / 微调 / RAG——面对 AI 知识需求的第一判断
# 用法：python labs/month08/m8l1_choose/test_choose.py


def choose_approach(knowledge):
    if knowledge.get("style_only"):
        return "finetune"                    # 只改风格/格式 -> 微调
    if knowledge.get("dynamic") or knowledge.get("need_citation") or knowledge.get("proprietary"):
        return "rag"                         # 时效/可溯源/私有 -> RAG
    return "prompt"                          # 通用知识 -> 提示即可


def run():
    assert choose_approach({"dynamic": True}) == "rag"
    assert choose_approach({"need_citation": True}) == "rag"
    assert choose_approach({"proprietary": True}) == "rag"
    assert choose_approach({"style_only": True}) == "finetune"
    assert choose_approach({}) == "prompt"
    print("✅ 全部通过: 按知识性质选 prompt/finetune/RAG")


if __name__ == "__main__":
    run()
