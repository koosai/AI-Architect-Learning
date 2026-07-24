# Month2 L10：事件总线  （对应 docs/02-system-design-bridge/communication-decoupling.mdx）
# 目标：发布订阅解耦 —— 生产者不认识任何消费者
# 用法：python labs/month02/m2l10_eventbus/test_event_bus.py


class EventBus:
    def __init__(self):
        self.subs = {}

    def subscribe(self, topic, handler):
        self.subs.setdefault(topic, []).append(handler)

    def publish(self, topic, event):
        n = 0
        for h in self.subs.get(topic, []):
            h(event)
            n += 1
        return n


def run():
    bus = EventBus()
    seen = []
    bus.subscribe("order", lambda e: seen.append(("inventory", e["id"])))
    bus.subscribe("order", lambda e: seen.append(("email", e["id"])))
    n = bus.publish("order", {"id": 7})
    assert n == 2 and ("inventory", 7) in seen and ("email", 7) in seen, (n, seen)
    assert bus.publish("unknown", {}) == 0   # 无订阅者
    print("✅ 全部通过: 发布订阅解耦，一次发布多方响应")


if __name__ == "__main__":
    run()
