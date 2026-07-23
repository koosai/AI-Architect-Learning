# Month4 L9：状态机（电梯）  （对应 docs/04-design-patterns-lld/state-machine-elevator.mdx）
# 目标：状态 + 合法转移集中成一张表，让非法转移被显式拒绝
# 用法：python labs/month04/m4l9_elevator/test_elevator.py

TRANSITIONS = {
    "idle": {"call": "moving"},
    "moving": {"arrive": "open"},
    "open": {"close": "idle"},
}


class Elevator:
    def __init__(self):
        self.state = "idle"

    def send(self, event):
        allowed = TRANSITIONS.get(self.state, {})
        if event not in allowed:
            raise ValueError(f"非法转移: {self.state} + {event}")
        self.state = allowed[event]
        return self.state


def run():
    e = Elevator()
    assert e.send("call") == "moving"
    assert e.send("arrive") == "open"
    assert e.send("close") == "idle"
    try:
        e.send("arrive")     # idle 状态不接受 arrive
        assert False, "非法转移应被拒绝"
    except ValueError:
        pass
    print("✅ 全部通过: 状态机（合法转移表，非法转移被拒）")


if __name__ == "__main__":
    run()
