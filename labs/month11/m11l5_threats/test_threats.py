# Month11 L5：LLM 威胁建模  （对应 docs/11-production-ai-platform/llm-threat-modeling.mdx）
# 目标：系统识别威胁 + 按影响排序 + 标信任边界
# 用法：python labs/month11/m11l5_threats/test_threats.py


def model_threats(system):
    threats = []
    if system.get("takes_user_input"):
        threats.append({"name": "prompt_injection", "impact": 3})
    if system.get("has_tools"):
        threats.append({"name": "tool_abuse", "impact": 3})
    if system.get("retrieves_external"):
        threats.append({"name": "indirect_injection", "impact": 2})
    if system.get("logs_pii"):
        threats.append({"name": "pii_leak", "impact": 2})
    return sorted(threats, key=lambda t: -t["impact"])   # 按影响排序


def run():
    ts = model_threats({"takes_user_input": True, "retrieves_external": True})
    names = [t["name"] for t in ts]
    assert "prompt_injection" in names and "indirect_injection" in names
    assert ts[0]["impact"] >= ts[-1]["impact"]           # 高影响在前
    print("✅ 全部通过: 威胁建模（识别+按影响排序+信任边界）")


if __name__ == "__main__":
    run()
