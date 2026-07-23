# Month10 L12：研究简报系统  （对应 docs/10-multi-agent-protocols/capstone-multi-agent.mdx）
# 目标：把 Month 10 全部能力整合成一个既强大又可控的研究简报系统
# 用法：python labs/month10/m10l12_briefing/test_briefing.py


class BriefingSystem:
    def __init__(self, perms, budget=10):
        self.perms = perms
        self.budget = budget
        self.trace = []

    def run(self, topic, subtopics):
        findings = []
        for st in subtopics:                       # supervisor 分配给多个 researcher
            if self.budget <= 0:
                self.trace.append((st, "skipped:budget"))   # 全局预算
                continue
            self.budget -= 1
            findings.append(f"finding on {st}")
            self.trace.append((st, "ok"))
        if "write" not in self.perms:              # 汇总需 write 权限（受控）
            return {"error": "no_write_permission"}
        return {"brief": f"# {topic}\n" + "\n".join(findings), "n_findings": len(findings)}


def run():
    bs = BriefingSystem(perms={"write"}, budget=2)
    out = bs.run("AI trends", ["llm", "rag", "agents"])
    assert out["n_findings"] == 2 and "AI trends" in out["brief"]   # 预算只够 2 个
    bs2 = BriefingSystem(perms=set())
    assert bs2.run("x", ["y"])["error"] == "no_write_permission"    # 无权限被挡
    print("✅ 全部通过: 研究简报系统（强大且可控：分工/预算/权限）")


if __name__ == "__main__":
    run()
