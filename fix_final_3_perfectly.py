import os
import re

docs_dir = r"c:\Users\K.K\OneDrive\Desktop\AI架构师教程\docs"

# Fix 1: replication.mdx
rep_path = os.path.join(docs_dir, "05-core-components", "replication.mdx")
if os.path.exists(rep_path):
    with open(rep_path, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('NodeA_S["("节点 A <br/>(新数据 X=v2)")"]', 'NodeA_S[("节点 A <br/>(新数据 X=v2)")]')
    c = c.replace('NodeB_S["("节点 B <br/>(新数据 X=v2)")"]', 'NodeB_S[("节点 B <br/>(新数据 X=v2)")]')
    c = c.replace('NodeC_S["("节点 C <br/>(旧数据 X=v1)")"]', 'NodeC_S[("节点 C <br/>(旧数据 X=v1)")]')
    c = c.replace('NodeA_W["("节点 A <br/>(新数据 Y=v2)")"]', 'NodeA_W[("节点 A <br/>(新数据 Y=v2)")]')
    c = c.replace('NodeB_W["("节点 B <br/>(旧数据 Y=v1)")"]', 'NodeB_W[("节点 B <br/>(旧数据 Y=v1)")]')
    c = c.replace('NodeC_W["("节点 C <br/>(旧数据 Y=v1)")"]', 'NodeC_W[("节点 C <br/>(旧数据 Y=v1)")]')
    with open(rep_path, 'w', encoding='utf-8') as f:
        f.write(c)

# Fix 2: enterprise-erp-integration.mdx
erp_path = os.path.join(docs_dir, "06-cloud-enterprise-industrial", "enterprise-erp-integration.mdx")
if os.path.exists(erp_path):
    with open(erp_path, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('Broker["["消息队列 / Event Broker"]"]', 'Broker["消息队列 / Event Broker"]')
    with open(erp_path, 'w', encoding='utf-8') as f:
        f.write(c)

# Fix 3: cdn.mdx
cdn_path = os.path.join(docs_dir, "04-atlas-case-studies", "tier1", "cdn.mdx")
if os.path.exists(cdn_path):
    with open(cdn_path, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('LDNS -->>Client: 4. 返回 Edge IP (1.2.3.4)', 'LDNS -->|4. 返回 Edge IP| Client')
    c = c.replace('%% alt 边缘缓存命中 (Cache Hit)\n    Edge1 -->>Client: 6. 200 OK (来自边缘 SSD/RAM 10ms)\n  %% else 缓存未命中 (Cache Miss)', 'Edge1 -->|6. 边缘缓存命中 200 OK| Client')
    c = c.replace('OriginDB -->>Edge1: 10. 返回源数据并缓存\n  end', 'OriginDB -->|10. 返回源数据并缓存| Edge1')
    with open(cdn_path, 'w', encoding='utf-8') as f:
        f.write(c)

print("Applied final 3 perfect fixes!")
