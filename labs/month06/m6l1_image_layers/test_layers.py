# Month6 L1：镜像层缓存  （对应 docs/06-cloud-enterprise-industrial/containers.mdx）
# 目标：层指纹 + 缓存命中 + 失效向上传播，体会层顺序为什么决定构建速度
# 用法：python labs/month06/m6l1_image_layers/test_layers.py
import hashlib


def build_layers(instructions, cache):
    fps = []
    parent = ""
    hits = builds = 0
    for ins in instructions:
        fp = hashlib.md5((parent + "|" + ins).encode()).hexdigest()[:8]  # 层指纹=父指纹+本层内容
        if fp in cache:
            hits += 1
        else:
            cache.add(fp)
            builds += 1
        fps.append(fp)
        parent = fp
    return fps, hits, builds


def run():
    cache = set()
    ins = ["FROM python", "COPY requirements", "RUN pip install", "COPY src"]
    _, _, b1 = build_layers(ins, cache)
    assert b1 == 4                               # 首次全部构建
    _, h2, b2 = build_layers(ins, cache)
    assert h2 == 4 and b2 == 0                    # 完全命中
    ins2 = ["FROM python", "COPY requirements", "RUN pip install", "COPY src2"]
    _, h3, b3 = build_layers(ins2, cache)
    assert h3 == 3 and b3 == 1                    # 只改末层：前 3 层命中
    ins3 = ["FROM python", "COPY reqs2", "RUN pip install", "COPY src2"]
    _, h4, b4 = build_layers(ins3, cache)
    assert h4 == 1 and b4 == 3                    # 改第 2 层：其上全部失效
    print("✅ 全部通过: 镜像层指纹/缓存命中/失效向上传播")


if __name__ == "__main__":
    run()
