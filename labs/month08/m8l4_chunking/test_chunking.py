# Month8 L4：分块  （对应 docs/08-rag/chunking.mdx）
# 目标：固定大小+重叠 与 按结构切，体会分块对检索粒度的影响
# 用法：python labs/month08/m8l4_chunking/test_chunking.py


def fixed_overlap(text, size, overlap):
    words = text.split()
    chunks = []
    step = size - overlap
    i = 0
    while i < len(words):
        chunks.append(" ".join(words[i:i + size]))
        i += step
    return chunks


def by_structure(sections):
    return [s.strip() for s in sections if s.strip()]   # 按段落/结构切，保语义边界


def run():
    chunks = fixed_overlap("a b c d e f", size=3, overlap=1)
    assert chunks[0] == "a b c" and chunks[1] == "c d e"   # 相邻块重叠 1 词
    secs = by_structure(["# Intro\npara1", "  ", "# Body\npara2"])
    assert len(secs) == 2                                   # 空段被丢弃
    print("✅ 全部通过: 固定+重叠分块 / 按结构切")


if __name__ == "__main__":
    run()
