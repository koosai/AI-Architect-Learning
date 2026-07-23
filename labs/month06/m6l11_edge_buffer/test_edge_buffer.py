# Month6 L11：工业边缘断网容错  （对应 docs/06-cloud-enterprise-industrial/industrial-edge-realtime.mdx）
# 目标：在线直发 / 离线缓冲 / 恢复补发 / 有界丢弃
# 用法：python labs/month06/m6l11_edge_buffer/test_edge_buffer.py


class EdgeBuffer:
    def __init__(self, capacity):
        self.cap = capacity
        self.buf = []
        self.sent = []
        self.dropped = 0
        self.online = True

    def emit(self, data):
        if self.online:
            self.sent.append(data)          # 在线直发
        elif len(self.buf) < self.cap:
            self.buf.append(data)           # 离线缓冲
        else:
            self.dropped += 1               # 超界有界丢弃

    def go_offline(self):
        self.online = False

    def recover(self):
        self.online = True
        self.sent.extend(self.buf)          # 恢复补发
        self.buf = []


def run():
    e = EdgeBuffer(capacity=2)
    e.emit("a")                             # 在线直发
    e.go_offline()
    e.emit("b")
    e.emit("c")
    e.emit("d")                             # 缓冲满 -> 丢弃 d
    assert e.dropped == 1 and len(e.buf) == 2
    e.recover()
    assert e.sent == ["a", "b", "c"] and e.buf == []   # 补发缓冲
    print("✅ 全部通过: 工业边缘（在线直发/离线缓冲/恢复补发/有界丢弃）")


if __name__ == "__main__":
    run()
