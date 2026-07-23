# Month6 L3：健康探针  （对应 docs/06-cloud-enterprise-industrial/config-secrets-probes.mdx）
# 目标：liveness/readiness/startup 分别驱动什么动作，避免依赖抖动引发 CrashLoop
# 用法：python labs/month06/m6l3_probes/test_probes.py


def probe_action(kind, healthy):
    if healthy:
        return "ok"
    return {
        "liveness": "restart",           # 存活失败 -> 重启容器
        "readiness": "remove_from_lb",   # 就绪失败 -> 摘出负载均衡（不重启）
        "startup": "wait",               # 启动探针 -> 等待，延迟其他探针
    }[kind]


def run():
    assert probe_action("liveness", False) == "restart"
    assert probe_action("readiness", False) == "remove_from_lb"  # 依赖抖动时摘除而非重启
    assert probe_action("startup", False) == "wait"
    assert probe_action("liveness", True) == "ok"
    print("✅ 全部通过: 探针（liveness重启 / readiness摘除 / startup等待）")


if __name__ == "__main__":
    run()
