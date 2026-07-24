# Atlas · Ray：共享内存对象存储（Plasma）  （对应 docs/atlas/ray.mdx）
# 目标：put 返回 ref，get 按 ref 取（零拷贝语义），引用计数归零回收
# 用法：python labs/month11/shared_mem_registry/test_object_store.py


class ObjectStore:
    def __init__(self):
        self.store = {}
        self.refcount = {}
        self.next_id = 0

    def put(self, obj):
        oid = self.next_id
        self.next_id += 1
        self.store[oid] = obj
        self.refcount[oid] = 1
        return oid                    # 返回对象引用（ObjectRef）

    def get(self, oid):
        return self.store.get(oid)    # 按 ref 取

    def incref(self, oid):
        self.refcount[oid] += 1

    def decref(self, oid):
        self.refcount[oid] -= 1
        if self.refcount[oid] <= 0:   # 引用归零 -> 回收
            del self.store[oid]
            del self.refcount[oid]


def run():
    s = ObjectStore()
    ref = s.put([1, 2, 3])
    assert s.get(ref) == [1, 2, 3]    # 按 ref 取
    s.incref(ref)
    s.decref(ref)
    s.decref(ref)
    assert s.get(ref) is None         # 引用归零 -> 回收
    print("✅ 全部通过: Ray 共享内存对象存储（ref + 引用计数回收）")


if __name__ == "__main__":
    run()
