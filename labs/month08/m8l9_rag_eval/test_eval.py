# Month8 L9：RAG 评测  （对应 docs/08-rag/rag-evaluation.mdx）
# 目标：检索指标 + 生成指标 + 诊断——RAG 优化最重要的方法论工具
# 用法：python labs/month08/m8l9_rag_eval/test_eval.py


def retrieval_recall(retrieved, relevant):
    return len(set(retrieved) & set(relevant)) / len(relevant)


def generation_faithful(answer_cites, retrieved_ids):
    if not answer_cites:
        return 0.0
    return len([c for c in answer_cites if c in retrieved_ids]) / len(answer_cites)


def diagnose(recall, faithful):
    if recall < 0.5:
        return "fix_retrieval"      # 召回差 -> 先修检索
    if faithful < 0.8:
        return "fix_generation"     # 检索好但答不忠实 -> 修生成
    return "ok"


def run():
    assert retrieval_recall(["a", "b"], ["a", "c"]) == 0.5
    assert generation_faithful(["a", "x"], {"a", "b"}) == 0.5
    assert diagnose(0.3, 1.0) == "fix_retrieval"
    assert diagnose(0.9, 0.5) == "fix_generation"
    assert diagnose(0.9, 0.9) == "ok"
    print("✅ 全部通过: 检索指标+生成指标+诊断定位")


if __name__ == "__main__":
    run()
