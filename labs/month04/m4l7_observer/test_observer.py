# Month4 L7：观察者模式  （对应 docs/04-design-patterns-lld/observer-pattern.mdx）
# 目标：一对多通知 + 解耦——发布者不认识订阅者，订阅者可增减
# 用法：python labs/month04/m4l7_observer/test_observer.py


class Subject:
    def __init__(self):
        self._subs = []

    def subscribe(self, fn):
        self._subs.append(fn)

    def unsubscribe(self, fn):
        self._subs.remove(fn)

    def notify(self, event):
        for s in self._subs:
            s(event)


def run():
    subj = Subject()
    log = []
    a = lambda e: log.append(("a", e))
    b = lambda e: log.append(("b", e))
    subj.subscribe(a)
    subj.subscribe(b)
    subj.notify("x")
    assert ("a", "x") in log and ("b", "x") in log
    subj.unsubscribe(a)
    log.clear()
    subj.notify("y")
    assert log == [("b", "y")], log        # a 已退订
    print("✅ 全部通过: 观察者（一对多通知，订阅者可增减）")


if __name__ == "__main__":
    run()
