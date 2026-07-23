# Month3 L9：消息队列可靠性  （对应 docs/03-data-cache-queue/message-queues.mdx）
# 目标：至少一次 + 重试 + 死信队列（DLQ）
# 用法：python labs/month03/m3l9_queue/test_queue.py


class Queue:
    def __init__(self, max_retries=2):
        self.q = []
        self.dlq = []       # 死信队列
        self.max = max_retries

    def send(self, msg):
        self.q.append({"msg": msg, "attempts": 0})

    def consume(self, handler):
        processed = []
        while self.q:
            item = self.q.pop(0)
            try:
                handler(item["msg"])
                processed.append(item["msg"])
            except Exception:
                item["attempts"] += 1
                if item["attempts"] > self.max:
                    self.dlq.append(item["msg"])   # 重试耗尽 -> 死信
                else:
                    self.q.append(item)            # 重新入队（至少一次）
        return processed


def run():
    q = Queue(max_retries=2)
    q.send("ok")
    q.send("poison")
    seen = []

    def handler(m):
        seen.append(m)
        if m == "poison":
            raise ValueError("bad")

    processed = q.consume(handler)
    assert "ok" in processed
    assert q.dlq == ["poison"], q.dlq            # 毒消息重试耗尽 -> 死信
    assert seen.count("poison") == 3, seen        # 1 次 + 2 次重试
    print("✅ 全部通过: 至少一次 / 重试 / 死信队列")


if __name__ == "__main__":
    run()
