# Month6 L4：HPA 弹性伸缩  （对应 docs/06-cloud-enterprise-industrial/autoscaling-rollout.mdx）
# 目标：期望副本 = 当前 × 指标/目标 + 容忍带 + 上下限
# 用法：python labs/month06/m6l4_hpa/test_hpa.py
import math


def desired_replicas(current, metric, target, tol=0.1, lo=1, hi=10):
    ratio = metric / target
    if abs(ratio - 1) <= tol:
        return current                       # 容忍带内不抖动
    want = math.ceil(current * ratio)
    return max(lo, min(hi, want))            # 上下限封顶


def run():
    assert desired_replicas(2, metric=80, target=50) == 4    # ceil(2*1.6)=4
    assert desired_replicas(4, metric=25, target=50) == 2    # ceil(4*0.5)=2
    assert desired_replicas(2, metric=52, target=50) == 2    # 容忍带内（4%）不动
    assert desired_replicas(2, metric=500, target=50) == 10  # 上限封顶
    assert desired_replicas(5, metric=1, target=50) == 1     # 下限保底
    print("✅ 全部通过: HPA（期望副本=ceil(当前×指标/目标)+容忍带+上下限）")


if __name__ == "__main__":
    run()
