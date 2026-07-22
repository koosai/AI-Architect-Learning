import os
import re

docs_dir = r"c:\Users\K.K\OneDrive\Desktop\AI架构师教程\docs"

def fix_line(line, in_seq):
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
        elif st.startswith('Note'):
            return l.replace('->', '→')
        return l

    # Flowchart fixes

    # 1. Restore Stadium Shape: Start("[Text")]) or Start("[Text]") -> Start(["Text"])
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\["\(?([^"\n]+)"?\)?\]\)', r'\1(["\2"])', l)

    # 2. Restore Database Shape: NodeID["("Text")"] -> NodeID[("Text")]
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\["\("([^"\n]+)"\)"\]', r'\1[("$2")]', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\["\("([^"\n]+)"\)"\]"\)', r'\1[("$2")]', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)"\)', r'\1[("$2")]', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\]"\)', r'\1[("$2")]', l)

    # 3. Restore Circle Shape: Ring("("Text")")) -> Ring(("Text"))
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)+', r'\1(("$2"))', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)\)"?\)', r'\1(("$2"))', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)', r'\1(("$2"))', l)

    # 4. Decision nodes: NodeID{Text} -> NodeID{"Clean Text"}
    def fix_decision(m):
        nid = m.group(1)
        inner = m.group(2).strip()
        if inner.startswith('"') and inner.endsWith('"') and not inner[1:-1].count('"'):
            return f'{nid}{{{inner}}}'
        clean = inner.replace('"', "'").replace('<br>', '<br/>')
        clean = re.sub(r'\|([^|\n]+)\|', r'abs(\1)', clean)
        return f'{nid}{{"{clean}"}}'

    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\{([^"\n\}]+)\}', fix_decision, l)

    # 5. Clean NodeID["..."] labels where label ends at final "]
    m_node = re.match(r'^(\s*)([A-Za-z0-9_\-\.]+)\s*\["(.*)"\](:::\w+)?$', l)
    if m_node:
        indent = m_node.group(1)
        nid = m_node.group(2)
        content = m_node.group(3)
        style = m_node.group(4) or ''

        clean = content.replace('"', "'").replace('[', '(').replace(']', ')')
        clean = re.sub(r"'\)$", '', clean)
        clean = re.sub(r"'\]$", '', clean)
        return f'{indent}{nid}["{clean}"]{style}'

    # 6. Clean subgraph titles: subgraph SubID ["Title"]
    m_sub = re.match(r'^(\s*)subgraph\s+([A-Za-z0-9_\-\.\u4e00-\u9fa5]+)\s*(.*)$', l)
    if m_sub:
        indent = m_sub.group(1)
        sub_id = m_sub.group(2)
        rest = m_sub.group(3).strip()

        clean_sub_id = re.sub(r'[^\w]', '_', sub_id)
        if clean_sub_id[0].isdigit():
            clean_sub_id = f"S_{clean_sub_id}"

        if rest:
            clean_title = rest.strip('[]"\'').replace('"', "'")
            return f'{indent}subgraph {clean_sub_id} ["{clean_title}"]'

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
                    fixed = fix_line(line, in_seq)
                    if fixed != line:
                        modified = True
                    new_lines.append(fixed)
                else:
                    new_lines.append(line)

            if modified:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.writelines(new_lines)
                fixed_files += 1

print(f"Cleaned node quotes until end across {fixed_files} files.")
