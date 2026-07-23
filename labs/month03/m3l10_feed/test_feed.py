# Month3 L10：Feed 写扩散  （对应 docs/03-data-cache-queue/feed-fanout.mdx）
# 目标：发帖时推送到粉丝收件箱（写扩散），体会读极快、写放大的取舍
# 用法：python labs/month03/m3l10_feed/test_feed.py


class FanoutFeed:
    def __init__(self, followers):
        self.followers = followers
        self.inbox = {}

    def post(self, author, item):
        for f in self.followers.get(author, []):
            self.inbox.setdefault(f, []).insert(0, item)   # 推到粉丝收件箱，最新在前

    def feed(self, user):
        return self.inbox.get(user, [])                    # 读收件箱，O(1)


def run():
    f = FanoutFeed(followers={"ada": ["bob", "cy"]})
    f.post("ada", "hello")
    f.post("ada", "world")
    assert f.feed("bob") == ["world", "hello"]   # 最新在前
    assert f.feed("cy") == ["world", "hello"]
    assert f.feed("nobody") == []
    print("✅ 全部通过: 写扩散扇出，读极快（代价：写放大）")


if __name__ == "__main__":
    run()
