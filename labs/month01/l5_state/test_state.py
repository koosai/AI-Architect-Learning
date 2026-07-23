# Lab L5：状态放在哪里  （对应 docs/01-foundations/state-and-storage.mdx）
# 目标：状态外移 + 依赖注入 —— 两个“无状态实例”共享注入的 store，才能水平扩展
# 用法：python labs/month01/l5_state/test_state.py


class Counter:
    def __init__(self, store):
        self.store = store  # 状态不在实例里，而在注入的共享 store

    def incr(self, key):
        self.store[key] = self.store.get(key, 0) + 1
        return self.store[key]


def run():
    shared = {}
    a = Counter(shared)
    b = Counter(shared)  # 模拟两个无状态实例（如两个 pod）
    a.incr("x")
    v = b.incr("x")  # b 能看到 a 的写入
    assert v == 2, v

    # 反例：各自持有本地状态 -> 各算各的（水平扩展下的经典 bug）
    class Bad:
        def __init__(self):
            self.n = 0

        def incr(self):
            self.n += 1
            return self.n

    x, y = Bad(), Bad()
    x.incr()
    assert y.incr() == 1, "本地状态不共享，正是要避免的问题"
    print("✅ 全部通过: 状态外移 + 依赖注入，多实例共享一致")


if __name__ == "__main__":
    run()
