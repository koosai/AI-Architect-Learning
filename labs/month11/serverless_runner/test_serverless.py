# Atlas · AWS Lambda：Serverless 冷启动  （对应 docs/atlas/aws-lambda.mdx）
# 目标：冷启动 vs 热调用；保持温实例复用以摊平延迟
# 用法：python labs/month11/serverless_runner/test_serverless.py


class ServerlessRunner:
    def __init__(self, keep_warm_ms=100):
        self.warm_until = -1
        self.keep = keep_warm_ms
        self.cold_starts = 0

    def invoke(self, now):
        if now <= self.warm_until:
            latency = 10                  # 热实例：快
        else:
            latency = 200                 # 冷启动：慢
            self.cold_starts += 1
        self.warm_until = now + self.keep
        return latency


def run():
    r = ServerlessRunner(keep_warm_ms=100)
    assert r.invoke(0) == 200 and r.cold_starts == 1     # 首次冷启动
    assert r.invoke(50) == 10                            # 100ms 内热调用
    assert r.invoke(500) == 200 and r.cold_starts == 2   # 超时后又冷启动
    print("✅ 全部通过: Serverless（冷启动 vs 热实例复用）")


if __name__ == "__main__":
    run()
