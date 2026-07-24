# Lab L11：同步/异步/队列  （对应 docs/01-foundations/sync-async-timeout.mdx）
# 目标：有界队列削峰；队满要背压(拒绝)而非无限堆积；Little's Law: L = λ * W
# 用法：python labs/month01/l11_async/test_queue.py


class BoundedQueue:
    def __init__(self, capacity):
        self.cap = capacity
        self.q = []

    def offer(self, item):
        if len(self.q) >= self.cap:
            return False           # 背压：拒绝入队，保护系统不被压垮
        self.q.append(item)
        return True

    def poll(self):
        return self.q.pop(0) if self.q else None


def little_law_L(arrival_rate, avg_wait):
    # L(系统内平均数量) = λ(到达率) * W(平均停留时间)
    return arrival_rate * avg_wait


def run():
    q = BoundedQueue(2)
    assert q.offer("a") and q.offer("b")
    assert q.offer("c") is False   # 队满 -> 背压拒绝
    assert q.poll() == "a"
    assert q.offer("c") is True    # 腾出空间后可入
    assert little_law_L(100, 0.2) == 20.0  # 100 req/s * 0.2s = 20 并发
    print("✅ 全部通过: 有界队列削峰 / 背压 / Little's Law")


if __name__ == "__main__":
    run()
