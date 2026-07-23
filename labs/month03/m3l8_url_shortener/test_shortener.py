# Month3 L8：短链服务  （对应 docs/03-data-cache-queue/url-shortener.mdx）
# 目标：发号 + base62 编码 + 映射存取，串成一个能用的服务
# 用法：python labs/month03/m3l8_url_shortener/test_shortener.py

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def to_base62(n):
    if n == 0:
        return "0"
    s = ""
    while n > 0:
        n, r = divmod(n, 62)
        s = BASE62[r] + s
    return s


class URLShortener:
    def __init__(self):
        self.seq = 0
        self.long_of = {}

    def shorten(self, long_url):
        self.seq += 1                    # 全局发号，保证唯一
        code = to_base62(self.seq)
        self.long_of[code] = long_url
        return code

    def resolve(self, code):
        return self.long_of.get(code)


def run():
    assert to_base62(0) == "0" and to_base62(61) == "Z" and to_base62(62) == "10"
    s = URLShortener()
    c1 = s.shorten("http://a.com")
    c2 = s.shorten("http://b.com")
    assert c1 != c2
    assert s.resolve(c1) == "http://a.com"
    assert s.resolve("nope") is None
    print("✅ 全部通过: 发号 + base62 + 映射存取")


if __name__ == "__main__":
    run()
