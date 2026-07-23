# Lab L6：幂等支付  （对应 docs/01-foundations/idempotency.mdx）
# 目标：idempotency key + 去重存储，重试不重复扣款
# 用法：python labs/month01/l6_idempotency/test_payment.py


class IdempotencyStore:
    def __init__(self):
        self._seen = {}

    def seen(self, k):
        return k in self._seen

    def get(self, k):
        return self._seen.get(k)

    def put(self, k, v):
        self._seen[k] = v


def process_payment(request_id, account, amount, balances, store):
    if store.seen(request_id):          # 见过 -> 直接返回旧结果，连余额都不碰
        return store.get(request_id)
    if balances.get(account, 0) < amount:
        res = {"status": "rejected", "reason": "insufficient", "balance": balances.get(account, 0)}
    else:
        balances[account] -= amount
        res = {"status": "ok", "balance": balances[account]}
    store.put(request_id, res)          # 成功/失败都记，保证同 key 返回同结果
    return res


def run():
    bal = {"ada": 100}
    s = IdempotencyStore()
    r1 = process_payment("req-1", "ada", 30, bal, s)
    r2 = process_payment("req-1", "ada", 30, bal, s)  # 同 key 重试
    assert r1 == r2 and bal["ada"] == 70, (r1, r2, bal)  # 只扣一次
    process_payment("req-2", "ada", 30, bal, s)          # 不同 key -> 真扣
    assert bal["ada"] == 40, bal
    r4 = process_payment("req-3", "ada", 999, bal, s)    # 余额不足
    assert r4["status"] == "rejected" and bal["ada"] == 40, (r4, bal)
    print("✅ 全部通过: 幂等键去重，重试不重复扣款")


if __name__ == "__main__":
    run()
