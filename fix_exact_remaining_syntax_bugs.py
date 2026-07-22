import os
import re

docs_dir = r"c:\Users\K.K\OneDrive\Desktop\AI架构师教程\docs"

def clean_line(line, in_seq):
    l = line.rstrip('\r\n')
    st = l.strip()

    if not st or st.startswith('%%') or st.startswith('flowchart') or st.startswith('sequenceDiagram') or st.startswith('mindmap') or st.startswith('graph'):
        return l

    if in_seq:
        if st.startswith('subgraph') or st.startswith('box'):
            indent = re.match(r'^\s*', l).group(0)
            title = re.sub(r'^\s*(subgraph|box)\s*(?:[A-Za-z0-9_\-\.]+\s*)?', '', l).strip()
            title = title.strip('[]"\'')
            title = title.replace('->', '→').replace('"', "'")
            return f'{indent}box "{title}"'
        return l

    # Flowchart fixes

    # 1. Subgraph titles with inner quotes or parens
    m_sub = re.match(r'^(\s*)subgraph\s+([A-Za-z0-9_\-\.\u4e00-\u9fa5]+)\s*\[?"?(.*?)"?\]?$', l)
    if m_sub:
        indent = m_sub.group(1)
        sub_id = m_sub.group(2)
        title = m_sub.group(3).strip()

        clean_sub_id = re.sub(r'[^\w]', '_', sub_id)
        if clean_sub_id[0].isdigit():
            clean_sub_id = f"S_{clean_sub_id}"

        if title:
            clean_title = title.replace('"', "'")
            return f'{indent}subgraph {clean_sub_id} ["{clean_title}"]'
        else:
            if clean_sub_id != sub_id:
                return f'{indent}subgraph {clean_sub_id} ["{sub_id}"]'
            else:
                return f'{indent}subgraph {clean_sub_id}'

    # 2. Circle shape: Name("("Text")")) -> Name(("Text"))
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)+', r'\1(("\2"))', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)\)"?\)', r'\1(("\2"))', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)', r'\1(("\2"))', l)

    # 3. Database shape: NodeID[("Text")]
    l = re.sub(r'\b([A-Za-z0-9_\-\.]+)\s*\["\("([^"\n]+)"\)"\]', r'\1[("$2")]', l)

    # 4. Clean stray closing quotes at end of node labels
    l = re.sub(r'"\]"\]$', '"]', l)
    l = re.sub(r'"\]"\)$', '"]', l)
    l = re.sub(r'"\)\)$', '"]', l)

    # 5. Fix inner double quotes & unescaped brackets inside NodeID["..."]
    # NodeID["..."] or inline NodeID["..."]
    def replace_node(m):
        nid = m.group(1)
        content = m.group(2)
        style = m.group(3) or ''

        clean = content.replace('"', "'").replace('[', '(').replace(']', ')')
        clean = re.sub(r"'\)$", '', clean)
        clean = re.sub(r"'\]$", '', clean)
        return f'{nid}["{clean}"]{style}'

    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\["([^"\n]+)"\](:::\w+)?', replace_node, l)

    return l

fixed_files = 0
for root, dirs, files in os.walk(docs_dir):
    for f in files:
        if f.endswith(".mdx") or f.endswith(".md"):
            filepath = os.path.join(root, f)
            with open(filepath, "r", encoding="utf-8") as file:
                lines = file.readlines()

            in_mermaid = False
            in_seq = False
            new_lines = []
            modified = False

            for line in lines:
                if line.strip().startswith("```mermaid"):
                    in_mermaid = True
                    in_seq = False
                    new_lines.append(line)
                    continue
                if in_mermaid and line.strip().startswith("```"):
                    in_mermaid = False
                    in_seq = False
                    new_lines.append(line)
                    continue
                if in_mermaid:
                    if 'sequenceDiagram' in line:
                        in_seq = True
                    fixed = clean_line(line, in_seq)
                    if fixed != line:
                        modified = True
                    new_lines.append(fixed)
                else:
                    new_lines.append(line)

            if modified:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.writelines(new_lines)
                fixed_files += 1

print(f"Fixed remaining syntax bugs across {fixed_files} files.")
