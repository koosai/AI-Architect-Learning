# Month5 L9：Quorum 法定人数读写  （对应 docs/05-core-components/replication.mdx）
# 目标：W+R>N 的法定人数读写，验证副本宕机下仍保证读到最新
# 用法：python labs/month05/m5l9_quorum/test_quorum.py


class QuorumStore:
    def __init__(self, n):
        self.n = n
        self.replicas = [None] * n     # 每个副本存 (value, version)

    def write(self, value, version, w, down=()):
        acked = 0
        for i in range(self.n):
            if i in down:
                continue
            self.replicas[i] = (value, version)
            acked += 1
            if acked >= w:
                break
        return acked >= w

    def read(self, r, down=()):
        got = []
        for i in range(self.n):
            if i in down:
                continue
            if self.replicas[i] is not None:
                got.append(self.replicas[i])
            if len(got) >= r:
                break
        if not got:
            return None
        return max(got, key=lambda x: x[1])[0]   # 取最高版本


def run():
    s = QuorumStore(n=3)            # N=3, W=2, R=2 -> W+R>N 保证读写集合相交
    s.replicas[2] = ("old", 0)     # 副本2 是旧值
    assert s.write("v1", 1, w=2)   # 写入副本 0,1（版本1）
    assert s.read(r=2) == "v1"                 # 读集合必与写集合相交 -> 见到版本1
    assert s.read(r=2, down={0}) == "v1"       # 读副本1(v1)+2(old) -> 取最高版本 v1
    print("✅ 全部通过: Quorum W+R>N（副本宕机仍读到最新）")


if __name__ == "__main__":
    run()
