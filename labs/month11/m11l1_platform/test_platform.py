# Month11 L1：为何要 AI 平台  （对应 docs/11-production-ai-platform/why-ai-platform.mdx）
# 目标：把多应用重复的护栏/成本/评估抽成共享平台；也理解何时不该抽
# 用法：python labs/month11/m11l1_platform/test_platform.py


def should_extract_to_platform(capability):
    # 多应用复用 + 横切关注点 -> 抽成平台；一次性/应用特有 -> 不抽
    return capability.get("used_by", 0) >= 2 and capability.get("cross_cutting", False)


def run():
    assert should_extract_to_platform({"used_by": 3, "cross_cutting": True}) is True    # 护栏/成本
    assert should_extract_to_platform({"used_by": 1, "cross_cutting": True}) is False   # 只一个用
    assert should_extract_to_platform({"used_by": 5, "cross_cutting": False}) is False  # 应用特有逻辑
    print("✅ 全部通过: 平台抽取（复用+集中治理；也知何时不抽）")


if __name__ == "__main__":
    run()
