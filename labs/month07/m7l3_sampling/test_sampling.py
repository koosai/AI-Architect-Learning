# Month7 L3：采样解码  （对应 docs/07-llm-systems/sampling-decoding.mdx）
# 目标：temperature 缩放 + top-p 截断，验证它们如何控制随机性与质量
# 用法：python labs/month07/m7l3_sampling/test_sampling.py
import math


def softmax_with_temp(logits, temp):
    scaled = [l / temp for l in logits]
    m = max(scaled)
    exps = [math.exp(x - m) for x in scaled]
    s = sum(exps)
    return [e / s for e in exps]


def top_p(probs, p):
    order = sorted(range(len(probs)), key=lambda i: -probs[i])
    cum = 0
    keep = set()
    for i in order:
        keep.add(i)
        cum += probs[i]
        if cum >= p:
            break
    filtered = [probs[i] if i in keep else 0 for i in range(len(probs))]
    s = sum(filtered)
    return [x / s for x in filtered]


def run():
    logits = [2.0, 1.0, 0.1]
    hot = softmax_with_temp(logits, temp=2.0)
    cold = softmax_with_temp(logits, temp=0.5)
    assert cold[0] > hot[0]              # 低温 -> 分布更集中（最高概率更大）
    assert abs(sum(hot) - 1) < 1e-9
    filt = top_p([0.6, 0.3, 0.1], p=0.8)
    assert filt[2] == 0                  # 累积 0.6+0.3=0.9>=0.8，尾部截断
    assert abs(sum(filt) - 1) < 1e-9
    print("✅ 全部通过: temperature 缩放 / top-p 截断")


if __name__ == "__main__":
    run()
