# Month5 L7：安全重试  （对应 docs/05-core-components/retry-backoff-timeout.mdx）
# 目标：超时→退避→抖动→上限→只重试可重试错误
# 用法：python labs/month05/m5l7_retry/test_retry.py
import random


def retry(fn, max_attempts=3, base=1, cap=10, retryable=(TimeoutError,), rng=None):
    rng = rng or random.Random(0)
    attempt = 0
    delays = []
    while True:
        attempt += 1
        try:
            return fn(attempt), delays
        except Exception as e:
            if not isinstance(e, retryable) or attempt >= max_attempts:
                raise                                    # 不可重试 / 到上限 -> 抛出
            backoff = min(cap, base * (2 ** (attempt - 1)))   # 指数退避 + 上限
            jittered = backoff * (0.5 + rng.random() * 0.5)   # 抖动
            delays.append({"raw": backoff, "jittered": jittered})


def run():
    calls = {"n": 0}

    def flaky(attempt):
        calls["n"] += 1
        if attempt < 3:
            raise TimeoutError()     # 前两次超时（可重试）
        return "ok"

    res, delays = retry(flaky, max_attempts=3)
    assert res == "ok" and calls["n"] == 3
    assert [d["raw"] for d in delays] == [1, 2]                       # 指数退避 1,2
    assert all(0.5 * d["raw"] <= d["jittered"] <= d["raw"] for d in delays)   # 抖动在范围内

    def fatal(attempt):
        raise ValueError("no retry")

    try:
        retry(fatal, max_attempts=3)
        assert False
    except ValueError:
        pass                          # 不可重试错误立即抛出，不重试
    print("✅ 全部通过: 安全重试（超时→退避→抖动→上限→只重试可重试错误）")


if __name__ == "__main__":
    run()
