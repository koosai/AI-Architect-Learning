# Month5 L6：断路器  （对应 docs/05-core-components/circuit-breaker.mdx）
# 目标：closed/open/half-open 三态机——阻断级联失败
# 用法：python labs/month05/m5l6_circuit_breaker/test_breaker.py


class CircuitBreaker:
    def __init__(self, threshold=3, cooldown=5):
        self.threshold = threshold
        self.cooldown = cooldown
        self.fails = 0
        self.state = "closed"
        self.opened = None

    def call(self, now, fn):
        if self.state == "open":
            if now - self.opened >= self.cooldown:
                self.state = "half_open"
            else:
                raise RuntimeError("circuit open")
        try:
            r = fn()
        except Exception:
            self.fails += 1
            if self.fails >= self.threshold:
                self.state = "open"
                self.opened = now
            raise
        self.fails = 0
        if self.state == "half_open":
            self.state = "closed"
        return r


def run():
    cb = CircuitBreaker(threshold=2, cooldown=5)

    def bad():
        raise ValueError()

    for _ in range(2):
        try:
            cb.call(0, bad)
        except ValueError:
            pass
    assert cb.state == "open"
    try:
        cb.call(1, lambda: "x")
        assert False
    except RuntimeError:
        pass
    assert cb.call(10, lambda: "ok") == "ok" and cb.state == "closed"
    print("✅ 全部通过: 断路器三态（阻断级联失败）")


if __name__ == "__main__":
    run()
