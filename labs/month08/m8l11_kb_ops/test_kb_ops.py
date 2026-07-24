# Month8 L11：知识库运维  （对应 docs/08-rag/knowledge-base-ops.mdx）
# 目标：增/改/删 + 去重 + 不留僵尸——知识库持续运维的核心
# 用法：python labs/month08/m8l11_kb_ops/test_kb_ops.py


class KnowledgeBase:
    def __init__(self):
        self.docs = {}
        self.hashes = {}     # content_hash -> doc_id

    def upsert(self, doc_id, content):
        h = hash(content)
        if h in self.hashes and self.hashes[h] != doc_id:
            return "duplicate"                    # 同内容不同 id -> 去重
        if doc_id in self.docs:
            self.hashes.pop(hash(self.docs[doc_id]), None)   # 清理旧内容哈希（不留僵尸）
        self.docs[doc_id] = content
        self.hashes[h] = doc_id
        return "upserted"

    def delete(self, doc_id):
        if doc_id in self.docs:
            self.hashes.pop(hash(self.docs[doc_id]), None)
            del self.docs[doc_id]
            return "deleted"
        return "not_found"


def run():
    kb = KnowledgeBase()
    assert kb.upsert("d1", "hello") == "upserted"
    assert kb.upsert("d1", "hello world") == "upserted"     # 改
    assert kb.upsert("d2", "hello world") == "duplicate"    # 与 d1 同内容
    assert kb.delete("d1") == "deleted"
    assert "d1" not in kb.docs and len(kb.hashes) == 0       # 无僵尸残留
    print("✅ 全部通过: 知识库增改删 + 去重 + 不留僵尸")


if __name__ == "__main__":
    run()
