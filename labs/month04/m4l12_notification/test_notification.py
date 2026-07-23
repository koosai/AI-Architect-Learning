# Month4 L12：通知系统综合  （对应 docs/04-design-patterns-lld/capstone-notification.mdx）
# 目标：策略/装饰器/观察者/DIP 组合成“处处可扩展、核心不改”的通知系统
# 用法：python labs/month04/m4l12_notification/test_notification.py


class NotificationSystem:
    def __init__(self):
        self.channels = []

    def add_channel(self, ch):
        self.channels.append(ch)          # DIP：注入渠道抽象（可调用）

    def notify(self, msg):
        return [ch(msg) for ch in self.channels]   # 观察者：广播到所有渠道


def email(m):
    return f"email:{m}"


def sms(m):
    return f"sms:{m}"


def timestamped(ch):
    # 装饰器：给渠道加时间戳前缀，不改原渠道
    def wrap(m):
        return ch(f"[t] {m}")
    return wrap


def run():
    system = NotificationSystem()
    system.add_channel(email)                 # 策略：不同渠道即不同算法
    system.add_channel(timestamped(sms))      # 装饰后的渠道
    out = system.notify("hi")
    assert out == ["email:hi", "sms:[t] hi"], out
    print("✅ 全部通过: 通知系统（策略/装饰器/观察者/DIP 组合，核心可扩展）")


if __name__ == "__main__":
    run()
