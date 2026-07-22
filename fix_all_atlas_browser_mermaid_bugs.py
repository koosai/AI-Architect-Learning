import os
import re

atlas_dir = r"c:\Users\K.K\OneDrive\Desktop\AI架构师教程\docs\atlas"

fixed_count = 0
for root, dirs, files in os.walk(atlas_dir):
    for f in files:
        if f.endswith('.mdx') or f.endswith('.md'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            orig = content

            # 1. Fix mindmap root("(Text")) -> root(("Text"))
            content = re.sub(r'root\("\((.*?)\)"\)', r'root(("\1"))', content)

            # 2. Fix flowchart <-->| -> <--->|
            content = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)<-->(\|[^|\n]+\|\s*[A-Za-z0-9_\-\.]+)', r'\1<--->\2', content)
            content = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)<-->(\s*[A-Za-z0-9_\-\.]+)', r'\1<--->\2', content)

            if content != orig:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                fixed_count += 1
                print(f"Fixed browser Mermaid compatibility in {os.path.basename(filepath)}")

print(f"\nTotal fixed files across Atlas: {fixed_count}")
