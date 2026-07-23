# Month11 L2：评估系统  （对应 docs/11-production-ai-platform/evaluation-systems.mdx）
# 目标：代表性评估集 + 分维度评分 + 回归门禁——AI 迭代的安全网
# 用法：python labs/month11/m11l2_eval/test_eval.py


def score_dims(pred, gold):
    return {
        "correct": 1.0 if pred["answer"] == gold["answer"] else 0.0,
        "cited": 1.0 if pred.get("cite") else 0.0,
    }


def eval_set(system, dataset):
    dims = {"correct": 0, "cited": 0}
    for q, gold in dataset:
        s = score_dims(system(q), gold)
        for k in dims:
            dims[k] += s[k]
    return {k: v / len(dataset) for k, v in dims.items()}


def gate(metrics, thresholds):
    return all(metrics[k] >= thresholds[k] for k in thresholds)


def run():
    ds = [("q1", {"answer": "A"}), ("q2", {"answer": "B"})]
    system = lambda q: {"answer": {"q1": "A", "q2": "B"}[q], "cite": "d1"}
    m = eval_set(system, ds)
    assert m["correct"] == 1.0 and m["cited"] == 1.0
    assert gate(m, {"correct": 0.9}) is True
    assert gate({"correct": 0.5}, {"correct": 0.9}) is False   # 回归门禁拦截退步
    print("✅ 全部通过: 评估集+分维度评分+回归门禁")


if __name__ == "__main__":
    run()
