# Month3 L3：MVCC 快照隔离  （对应 docs/03-data-cache-queue/transactions-isolation.mdx）
# 目标：理解快照隔离为什么“读不阻塞写”，以及和加锁的根本不同
# 用法：python labs/month03/m3l3_mvcc/test_mvcc.py


class MVCCStore:
    def __init__(self):
        self.rows = {}          # key -> [{"v":..., "txid":...}, ...]
        self.txid = 0
        self.committed = set()

    def begin(self):
        self.txid += 1
        return self.txid

    def write(self, txid, key, value):
        self.rows.setdefault(key, []).append({"v": value, "txid": txid})

    def commit(self, txid):
        self.committed.add(txid)

    def read(self, snapshot_txid, key):
        # 只看到 txid <= 快照 且已提交的最新版本
        best = None
        for ver in self.rows.get(key, []):
            if ver["txid"] <= snapshot_txid and ver["txid"] in self.committed:
                if best is None or ver["txid"] > best["txid"]:
                    best = ver
        return best["v"] if best else None


def run():
    s = MVCCStore()
    t1 = s.begin()
    s.write(t1, "x", 10)
    s.commit(t1)
    reader = s.begin()               # reader 拿到当前快照
    t3 = s.begin()
    s.write(t3, "x", 20)             # 写事务进行中（未提交）
    assert s.read(reader, "x") == 10, "读不阻塞写，且看不到未提交的 20"
    s.commit(t3)
    assert s.read(reader, "x") == 10, "老快照仍看到 10（快照隔离）"
    new_reader = s.begin()
    assert s.read(new_reader, "x") == 20, "新快照才看到 20"
    print("✅ 全部通过: MVCC 快照隔离，读不阻塞写")


if __name__ == "__main__":
    run()
