# Month3 L12：Feed 服务综合  （对应 docs/03-data-cache-queue/capstone-feed.mdx）
# 目标：把本月知识整合成一个能用的 feed 服务（发号/存储/写扩散/时间线）
# 用法：python labs/month03/m3l12_feed_capstone/test_feed_service.py


class FeedService:
    def __init__(self, followers):
        self.followers = followers
        self.inbox = {}      # user -> [post_id, ...]（写扩散收件箱）
        self.posts = {}      # post_id -> {author, text}
        self.seq = 0

    def post(self, author, text):
        self.seq += 1
        pid = self.seq
        self.posts[pid] = {"author": author, "text": text}
        for f in self.followers.get(author, []):
            self.inbox.setdefault(f, []).insert(0, pid)
        return pid

    def timeline(self, user, limit=10):
        return [self.posts[pid] for pid in self.inbox.get(user, [])[:limit]]


def run():
    svc = FeedService(followers={"ada": ["bob"]})
    svc.post("ada", "hi")
    svc.post("ada", "yo")
    tl = svc.timeline("bob")
    assert [p["text"] for p in tl] == ["yo", "hi"], tl   # 最新在前
    assert svc.timeline("nobody") == []
    print("✅ 全部通过: feed 服务整合（发号/存储/写扩散/时间线）")


if __name__ == "__main__":
    run()
