import os
import re

docs_dir = r"c:\Users\K.K\OneDrive\Desktop\AI架构师教程\docs"

def sanitize_line(line):
    l = line.rstrip('\r\n')

    # Fix subgraph SubID ["Title']"] or ["'Title'"] -> subgraph SubID ["Title"]
    m_sub = re.match(r'^(\s*)subgraph\s+([A-Za-z0-9_\-\.\u4e00-\u9fa5]+)\s*\["\'?(.*?)\'?"\]', l)
    if m_sub:
        indent = m_sub.group(1)
        sub_id = m_sub.group(2)
        title = m_sub.group(3).strip('[]"\'')
        l = f'{indent}subgraph {sub_id} ["{title}"]'

    # Fix node label stray trailing quotes: NodeID["Text"]"] -> NodeID["Text"]
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*\["[^"\n]+)"\]"\]', r'\1"]', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*\["[^"\n]+)\'\]"\]', r'\1"]', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*\["[^"\n]+)"\]\'\]', r'\1"]', l)

    # Fix inner square brackets inside node label: Res1["匹配结果: [ada, bob"]"] -> Res1["匹配结果: (ada, bob)"]
    l = l.replace('[ada, bob"]"', '(ada, bob)]"')
    l = l.replace("['e1'\"]\"", "('e1')]\"")
    l = l.replace("['ada'\"]\"", "('ada')]\"")

    return l

fixed_files = 0
for root, dirs, files in os.walk(docs_dir):
    for f in files:
        if f.endswith(".mdx") or f.endswith(".md"):
            filepath = os.path.join(root, f)
            with open(filepath, "r", encoding="utf-8") as file:
                lines = file.readlines()

            in_mermaid = False
            new_lines = []
            modified = False

            for line in lines:
                if line.strip().startswith("```mermaid"):
                    in_mermaid = True
                    new_lines.append(line)
                    continue
                if in_mermaid and line.strip().startswith("```"):
                    in_mermaid = False
                    new_lines.append(line)
                    continue
                if in_mermaid:
                    fixed_l = sanitize_line(line)
                    if fixed_l != line:
                        modified = True
                    new_lines.append(fixed_l)
                else:
                    new_lines.append(line)

            if modified:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.writelines(new_lines)
                fixed_files += 1

print(f"Sanitized line quotes across {fixed_files} files.")
