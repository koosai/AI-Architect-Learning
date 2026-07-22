import os
import re

docs_dir = r"c:\Users\K.K\OneDrive\Desktop\AI架构师教程\docs"

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content

    # 1. npm.mdx: Node ID "CDN POP" -> "CDN_POP"
    if 'npm.mdx' in filepath:
        content = content.replace('CDN POP', 'CDN_POP')

    # 2. postgresql.mdx: Fix [105"]) and Note over in flowchart
    if 'postgresql.mdx' in filepath:
        content = content.replace('活跃列表=[105"])', '活跃列表=105)')
        content = re.sub(
            r'Note over Reader,\s*TupleV1:\s*(.*)',
            r'Note1["\1"]\n  Reader -.-> Note1\n  TupleV1 -.-> Note1',
            content
        )
        content = re.sub(
            r'Note over Reader,\s*TupleV2:\s*(.*)',
            r'Note2["\1"]\n  Reader -.-> Note2\n  TupleV2 -.-> Note2',
            content
        )

    # 3. sqlite.mdx: Fix Mem["])
    if 'sqlite.mdx' in filepath:
        content = content.replace('Mem["])', 'Mem)')

    # 4. kafka.mdx: Fix <--| and circle shape
    if 'kafka.mdx' in filepath:
        content = content.replace('Consumer["消费者应用 (Consumer App)"]:::client <--|2. 主动拉取消息流 (Pull Model)| KafkaCluster', 'KafkaCluster -->|2. 主动拉取消息流 (Pull Model)| Consumer["消费者应用 (Consumer App)"]:::client')
        content = content.replace('TieredStorage["("对象存储 (AWS S3 / GCS)")"]:::third', 'TieredStorage[("对象存储 (AWS S3 / GCS)")]:::third')

    # 5. gitlab-ci.mdx: Fix <--|
    if 'gitlab-ci.mdx' in filepath:
        content = content.replace('TestJobPod <--|7. 下载前置编译产物| ArtifactBucket', 'ArtifactBucket -->|7. 下载前置编译产物| TestJobPod')

    # 6. elasticsearch.mdx: Fix Doc#2[Del"]) and Note over
    if 'elasticsearch.mdx' in filepath:
        content = content.replace('[Del"])', ' (Del)')
        content = re.sub(
            r'Note over S4:\s*(.*)',
            r'NoteS4["\1"]\n    S4 -.-> NoteS4',
            content
        )

    # 7. cdn.mdx: Fix alt/else in flowchart
    if 'cdn.mdx' in filepath:
        content = content.replace('alt 边缘缓存命中 (Cache Hit)', '%% alt 边缘缓存命中 (Cache Hit)')
        content = content.replace('else 缓存未命中 (Cache Miss)', '%% else 缓存未命中 (Cache Miss)')

    # 8. advanced-rag.mdx: Fix ['public'"])
    if 'advanced-rag.mdx' in filepath:
        content = content.replace("['public'\"])", "'public'")

    # 9. scaling-strategies.mdx: Fix Ring("("...")")
    if 'scaling-strategies.mdx' in filepath:
        content = content.replace('Ring("("哈希空间环 (0 ~ 2^32 - 1")"))', 'Ring(("哈希空间环 (0 ~ 2^32 - 1)"))')

    # 10. replication.mdx: Fix StrongQuorum subgraph title inner quotes
    if 'replication.mdx' in filepath:
        content = content.replace('("W + R = 4 > 3")', "'W + R = 4 > 3'")
        content = content.replace('("W + R = 3 <= 3")', "'W + R = 3 <= 3'")

    # 11. autoscaling-rollout.mdx: Fix Start shape
    if 'autoscaling-rollout.mdx' in filepath:
        content = content.replace('Start("[定期触发计算 (默认 15s")])', 'Start(["定期触发计算 (默认 15s)"])')

    # 12. enterprise-erp-integration.mdx: Fix <--> and circle shape
    if 'enterprise-erp-integration.mdx' in filepath:
        content = content.replace('<-->', '<--->')
        content = content.replace('("(Sys A"))', '(("Sys A"))')
        content = content.replace('("(Sys B"))', '(("Sys B"))')
        content = content.replace('("(Sys C"))', '(("Sys C"))')
        content = content.replace('("(Sys D"))', '(("Sys D"))')

    if content != orig:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")

for root, dirs, files in os.walk(docs_dir):
    for file in files:
        if file.endswith('.mdx') or file.endswith('.md'):
            fix_file(os.path.join(root, file))
