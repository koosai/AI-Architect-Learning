# Month5 L5：限流  （对应 docs/05-core-components/rate-limiting.mdx）
# 目标：按时间补令牌 + 突发 + 拒绝——最常用的限流算法
# 用法：python labs/month05/m5l5_rate_limit/test_rate_limit.py


class RateLimiter:
    def __init__(self, rate, burst):
        self.rate = rate        # 每秒补充令牌数
        self.burst = burst      # 桶容量（允许的突发量）
        self.tokens = burst
        self.last = 0.0

    def allow(self, now):
        self.tokens = min(self.burst, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


def run():
    rl = RateLimiter(rate=1, burst=3)
    assert sum(rl.allow(0) for _ in range(5)) == 3   # 突发上限 = burst = 3
    assert rl.allow(0) is False                      # 桶空 -> 拒绝
    assert rl.allow(2) is True                       # 2 秒补 2 个 -> 放行
    print("✅ 全部通过: 限流（补令牌 + 突发 + 拒绝）")


if __name__ == "__main__":
    run()
