# Month3 L1：LSM 存储引擎  （对应 docs/03-data-cache-queue/storage-engines.mdx）
# 目标：理解 LSM 为什么写快、读放大、为什么需要 compaction
# 用法：python labs/month03/m3l1_lsm/test_lsm.py


class LSMTree:
    def __init__(self, memtable_limit=3):
        self.memtable = {}
        self.sstables = []          # 不可变、从旧到新
        self.limit = memtable_limit

    def put(self, k, v):
        self.memtable[k] = v        # 写只落 memtable（顺序、极快）
        if len(self.memtable) >= self.limit:
            self.flush()

    def flush(self):
        if self.memtable:
            self.sstables.append(dict(self.memtable))
            self.memtable = {}

    def get(self, k):
        if k in self.memtable:
            return self.memtable[k]
        for sst in reversed(self.sstables):   # 从新到旧逐层找 -> 读放大
            if k in sst:
                return sst[k]
        return None

    def compact(self):
        merged = {}
        for sst in self.sstables:   # 旧 -> 新覆盖
            merged.update(sst)
        self.sstables = [merged] if merged else []


def run():
    t = LSMTree(memtable_limit=2)
    t.put("a", 1)
    t.put("b", 1)   # 触发 flush -> sst1
    t.put("a", 2)
    t.put("c", 3)   # 触发 flush -> sst2
    assert t.get("a") == 2, "读到最新版本"
    assert t.get("b") == 1
    assert len(t.sstables) == 2, "写只追加，但读要翻多层（读放大）"
    t.compact()
    assert len(t.sstables) == 1 and t.get("a") == 2, "compaction 合并层"
    print("✅ 全部通过: LSM memtable/flush/读放大/compaction")


if __name__ == "__main__":
    run()
