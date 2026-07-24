# Month2 L9：LLD 令牌桶限流器  （对应 docs/02-system-design-bridge/lld-classes.mdx）
# 目标：把一个 HLD 组件落成具体的类：清晰接口 / 内部状态 / 正确算法
# 用法：python labs/month02/m2l9_lld/test_rate_limiter.py


class TokenBucket:
    def __init__(self, capacity, refill_per_sec):
        self.capacity = capacity
        self.tokens = capacity
        self.refill = refill_per_sec
        self.last = 0.0

    def allow(self, now, cost=1):
        # 按时间流逝补充令牌（不超过容量），够则扣减放行
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.refill)
        self.last = now
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False


def run():
    tb = TokenBucket(capacity=2, refill_per_sec=1)
    assert tb.allow(0) and tb.allow(0)   # 初始 2 个令牌
    assert tb.allow(0) is False          # 桶空 -> 拒绝
    assert tb.allow(1) is True           # 1 秒后补 1 个 -> 放行
    assert tb.allow(1) is False          # 又空
    print("✅ 全部通过: 令牌桶限流（容量/补充/扣减）")


if __name__ == "__main__":
    run()
