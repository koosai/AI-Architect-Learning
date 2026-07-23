# Month6 L2：调和循环  （对应 docs/06-cloud-enterprise-industrial/kubernetes-basics.mdx）
# 目标：读期望→看实际→算差异→行动——K8s 自愈与声明式的核心
# 用法：python labs/month06/m6l2_reconcile/test_reconcile.py


def reconcile(desired, actual):
    if actual < desired:
        return ("scale_up", desired - actual)
    if actual > desired:
        return ("scale_down", actual - desired)
    return ("noop", 0)


def run():
    assert reconcile(3, 1) == ("scale_up", 2)
    assert reconcile(2, 5) == ("scale_down", 3)
    assert reconcile(3, 3) == ("noop", 0)
    # 自愈：一个 pod 崩了（actual 降），下一轮 reconcile 自动补齐
    actual = 3 - 1
    assert reconcile(3, actual) == ("scale_up", 1)
    print("✅ 全部通过: 调和循环（期望→实际→差异→行动，声明式自愈）")


if __name__ == "__main__":
    run()
