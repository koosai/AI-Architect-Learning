# Month6 L9：多云抽象  （对应 docs/06-cloud-enterprise-industrial/multi-cloud.mdx）
# 目标：用 DIP + 适配器把业务和具体云解耦——保留可移植性的同时理解其边界
# 用法：python labs/month06/m6l9_cloud_abstraction/test_abstraction.py


class BlobStore:   # 抽象接口（约定）
    def put(self, k, v):
        raise NotImplementedError

    def get(self, k):
        raise NotImplementedError


class S3Adapter(BlobStore):
    def __init__(self):
        self._b = {}

    def put(self, k, v):
        self._b["s3:" + k] = v

    def get(self, k):
        return self._b.get("s3:" + k)


class GCSAdapter(BlobStore):
    def __init__(self):
        self._b = {}

    def put(self, k, v):
        self._b["gcs:" + k] = v

    def get(self, k):
        return self._b.get("gcs:" + k)


def backup(store, name, data):
    store.put(name, data)          # 业务代码只认抽象，不认具体云
    return store.get(name)


def run():
    assert backup(S3Adapter(), "a", "x") == "x"
    assert backup(GCSAdapter(), "a", "x") == "x"   # 换云=换适配器，业务不改
    print("✅ 全部通过: 多云抽象（DIP+适配器，业务与具体云解耦）")


if __name__ == "__main__":
    run()
