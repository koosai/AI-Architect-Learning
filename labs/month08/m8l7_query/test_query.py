# Month8 L7：查询变换  （对应 docs/08-rag/query-transformation.mdx）
# 目标：改写 + 多查询扩展 + 合并去重，体会优化“问法”如何提升召回
# 用法：python labs/month08/m8l7_query/test_query.py


def rewrite(query):
    return query.strip().lower().replace("pls", "please")


def multi_query(query):
    return [query, query + " tutorial", query + " example"]   # 一问变多问


def merge_dedup(result_lists):
    seen = []
    for lst in result_lists:
        for x in lst:
            if x not in seen:
                seen.append(x)      # 合并去重，保序
    return seen


def run():
    assert rewrite("  Pls Help ") == "please help"
    qs = multi_query("python")
    assert len(qs) == 3 and "python tutorial" in qs
    assert merge_dedup([["a", "b"], ["b", "c"], ["a", "d"]]) == ["a", "b", "c", "d"]
    print("✅ 全部通过: 查询改写 + 多查询扩展 + 合并去重")


if __name__ == "__main__":
    run()
