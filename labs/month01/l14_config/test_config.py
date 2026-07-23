# Lab L14：配置与部署  （对应 docs/01-foundations/config-and-deploy.mdx）
# 目标：配置与代码分离；环境变量优先；密钥必须来自环境，绝不硬编码
# 用法：python labs/month01/l14_config/test_config.py


class ConfigError(Exception):
    pass


def load_config(defaults, env):
    cfg = dict(defaults)
    for k in list(cfg.keys()):
        if k in env:
            cfg[k] = env[k]           # 环境变量覆盖默认值
    if not env.get("SECRET_KEY"):
        raise ConfigError("SECRET_KEY 必须由环境提供，不能硬编码")  # 密钥强制来自环境
    cfg["SECRET_KEY"] = env["SECRET_KEY"]
    return cfg


def run():
    defaults = {"host": "localhost", "port": "5432"}
    cfg = load_config(defaults, {"port": "6000", "SECRET_KEY": "s3cr3t"})
    assert cfg["host"] == "localhost" and cfg["port"] == "6000", cfg  # env 覆盖 port
    assert cfg["SECRET_KEY"] == "s3cr3t"
    try:
        load_config(defaults, {"port": "6000"})  # 无密钥
        assert False, "应拒绝启动"
    except ConfigError:
        pass
    print("✅ 全部通过: 配置分离 / env 优先 / 密钥来自环境")


if __name__ == "__main__":
    run()
