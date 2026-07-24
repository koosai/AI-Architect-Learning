# Month6 L12：云原生交付流水线  （对应 docs/06-cloud-enterprise-industrial/capstone-cloud-native.mdx）
# 目标：声明式 + 自动化 + 安全回滚——把本月环节组装成一条可跑的交付流水线
# 用法：python labs/month06/m6l12_delivery/test_delivery.py


def deliver(desired_version, build_ok=True, health_ok=True):
    log = [("build", desired_version)]
    if not build_ok:
        return log + [("fail", "build")], "prev"
    current = desired_version
    log.append(("deploy", current))
    if not health_ok:
        log.append(("rollback", "prev"))     # 健康检查失败 -> 自动回滚
        return log, "prev"
    return log, current


def run():
    log, ver = deliver("v2")
    assert ver == "v2" and ("deploy", "v2") in log
    log2, ver2 = deliver("v3", health_ok=False)
    assert ver2 == "prev" and ("rollback", "prev") in log2   # 失败自动回滚
    log3, ver3 = deliver("v4", build_ok=False)
    assert ver3 == "prev" and ("deploy", "v4") not in log3    # 构建失败不部署
    print("✅ 全部通过: 交付流水线（声明式+自动化+安全回滚）")


if __name__ == "__main__":
    run()
