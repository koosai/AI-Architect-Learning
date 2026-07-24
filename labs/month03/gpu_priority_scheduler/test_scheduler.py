# Atlas · Midjourney：GPU Fast/Relax 双队列调度器
#   （对应 docs/atlas/midjourney.mdx 的动手练习）
# 目标：Fast 队列（付费高优先）优先占用 GPU，剩余产能才给 Relax 队列
# 用法：python labs/month03/gpu_priority_scheduler/test_scheduler.py


class GPUScheduler:
    def __init__(self, num_gpus):
        self.num_gpus = num_gpus
        self.fast = []      # 高优先队列
        self.relax = []     # 低优先队列

    def submit(self, job, mode):
        (self.fast if mode == "fast" else self.relax).append(job)

    def schedule(self):
        # 每轮：先派 fast，剩余 GPU 槽位再派 relax
        assigned = []
        slots = self.num_gpus
        for q in (self.fast, self.relax):
            while q and slots > 0:
                assigned.append(q.pop(0))
                slots -= 1
        return assigned


def run():
    s = GPUScheduler(num_gpus=2)
    s.submit("r1", "relax")
    s.submit("f1", "fast")
    s.submit("f2", "fast")
    s.submit("r2", "relax")
    assert s.schedule() == ["f1", "f2"]   # fast 优先占满 2 张卡
    assert s.schedule() == ["r1", "r2"]   # 下一轮才轮到 relax
    print("✅ 全部通过: GPU Fast/Relax 双队列优先调度")


if __name__ == "__main__":
    run()
