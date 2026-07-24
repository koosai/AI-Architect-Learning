# Atlas · Perplexity：抓取结果重排 + 引用  （对应 docs/atlas/perplexity.mdx）
# 目标：抓取搜索结果 -> 按与 query 相关度重排 -> 带来源引用
# 用法：python labs/month08/scraped_rerank/test_scraped_rerank.py


def rerank(query_terms, results):
    def score(r):
        return sum(1 for t in query_terms if t in r["snippet"])
    return sorted(results, key=lambda r: -score(r))


def answer_with_citation(query_terms, results):
    top = rerank(query_terms, results)[0]
    return {"answer": top["snippet"], "source": top["url"]}


def run():
    results = [{"url": "a.com", "snippet": "cats are cute"}, {"url": "b.com", "snippet": "dogs run fast"}]
    out = answer_with_citation(["cats"], results)
    assert out["source"] == "a.com" and "cats" in out["answer"]   # 带来源引用
    print("✅ 全部通过: 搜索抓取+重排+带引用（Perplexity）")


if __name__ == "__main__":
    run()
