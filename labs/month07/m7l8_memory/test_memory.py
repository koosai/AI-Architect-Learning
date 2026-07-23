# Month7 L8：多轮记忆  （对应 docs/07-llm-systems/context-memory.mdx）
# 目标：最近原文 + 更早摘要 + token 预算——多轮 LLM 应用的记忆核心
# 用法：python labs/month07/m7l8_memory/test_memory.py


def build_memory(turns, budget, recent_keep=2):
    recent = turns[-recent_keep:]
    older = turns[:-recent_keep]
    mem = []
    if older:
        mem.append(f"[摘要:{len(older)}轮]")     # 更早的压成摘要
    mem.extend(recent)                            # 最近的保留原文
    while sum(len(x) for x in mem) > budget and len(mem) > 1:
        mem.pop(0)                                # 超预算则从最旧开始丢
    return mem


def run():
    turns = ["t1_hello", "t2_world", "t3_foo", "t4_bar"]
    mem = build_memory(turns, budget=100, recent_keep=2)
    assert mem[0].startswith("[摘要") and "2轮" in mem[0]   # 前 2 轮被摘要
    assert "t3_foo" in mem and "t4_bar" in mem             # 最近 2 轮保留原文
    print("✅ 全部通过: 记忆（最近原文 + 更早摘要 + 预算控制）")


if __name__ == "__main__":
    run()
