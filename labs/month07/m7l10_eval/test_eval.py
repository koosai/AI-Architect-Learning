# Month7 L10：LLM 评测  （对应 docs/07-llm-systems/llm-evaluation.mdx）
# 目标：评测集 + 打分 + 回归对比——给 LLM 系统装上回归测试
# 用法：python labs/month07/m7l10_eval/test_eval.py


def score(prediction, expected):
    return 1.0 if prediction.strip().lower() == expected.strip().lower() else 0.0


def evaluate(system, dataset):
    total = sum(score(system(q), a) for q, a in dataset)
    return total / len(dataset)


def regression(old_acc, new_acc):
    return "pass" if new_acc >= old_acc else "regressed"


def run():
    ds = [("2+2", "4"), ("cap of France", "Paris")]
    good = lambda q: {"2+2": "4", "cap of France": "Paris"}[q]
    bad = lambda q: {"2+2": "4", "cap of France": "London"}[q]
    assert evaluate(good, ds) == 1.0
    assert evaluate(bad, ds) == 0.5
    assert regression(1.0, 0.5) == "regressed"   # 新版本退步被抓
    assert regression(0.5, 0.8) == "pass"
    print("✅ 全部通过: 评测集/打分/回归对比")


if __name__ == "__main__":
    run()
