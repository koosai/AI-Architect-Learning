# Month2 L11：断路器  （对应 docs/02-system-design-bridge/reliability-fault-tolerance.mdx）
# 目标：把“依赖挂了就跳闸保护”做成 closed/open/half-open 状态机
# 用法：python labs/month02/m2l11_circuit_breaker/test_breaker.py


class CircuitBreaker:
    def __init__(self, fail_threshold=3, recovery_time=5):
        self.fail_threshold = fail_threshold
        self.recovery_time = recovery_time
        self.failures = 0
        self.state = "closed"
        self.opened_at = None

    def call(self, now, fn):
        if self.state == "open":
            if now - self.opened_at >= self.recovery_time:
                self.state = "half_open"          # 冷却够了，放一个试探
            else:
                raise RuntimeError("circuit open: fail fast")  # 跳闸：快速失败
        try:
            r = fn()
        except Exception:
            self.failures += 1
            if self.failures >= self.fail_threshold:
                self.state = "open"
                self.opened_at = now
            raise
        if self.state == "half_open":
            self.state = "closed"                 # 试探成功 -> 恢复
        self.failures = 0
        return r


def run():
    cb = CircuitBreaker(fail_threshold=2, recovery_time=5)

    def bad():
        raise ValueError("down")

    def good():
        return "ok"

    for _ in range(2):
        try:
            cb.call(0, bad)
        except ValueError:
            pass
    assert cb.state == "open"                      # 连续失败 -> 跳闸
    try:
        cb.call(1, good)
        assert False, "冷却期内应 fail fast"
    except RuntimeError:
        pass
    assert cb.call(10, good) == "ok"               # 冷却后半开试探成功
    assert cb.state == "closed"                    # -> 恢复
    print("✅ 全部通过: 断路器 closed/open/half-open 状态机")


if __name__ == "__main__":
    run()
