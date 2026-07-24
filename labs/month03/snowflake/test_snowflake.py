# Atlas · Discord：Snowflake ID 生成器  （对应 docs/atlas/discord.mdx）
# 目标：64 位 ID = 时间戳 + 机器 ID + 序列号，全局唯一且时间有序
# 用法：python labs/month03/snowflake/test_snowflake.py


class SnowflakeGen:
    def __init__(self, worker_id):
        self.worker = worker_id
        self.seq = 0
        self.last_ms = -1

    def next_id(self, now_ms):
        if now_ms == self.last_ms:
            self.seq = (self.seq + 1) & 0xFFF     # 同毫秒内递增序列（12 位）
        else:
            self.seq = 0
            self.last_ms = now_ms
        return (now_ms << 22) | (self.worker << 12) | self.seq


def run():
    g = SnowflakeGen(worker_id=1)
    a = g.next_id(1000)
    b = g.next_id(1000)
    c = g.next_id(1001)
    assert a < b < c              # 时间有序
    assert len({a, b, c}) == 3    # 全局唯一
    assert (a >> 22) == 1000      # 高位是时间戳
    print("✅ 全部通过: Snowflake ID（时间戳+机器+序列，有序且唯一）")


if __name__ == "__main__":
    run()
