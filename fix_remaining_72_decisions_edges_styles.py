import os
import re

docs_dir = r"c:\Users\K.K\OneDrive\Desktop\AI架构师教程\docs"

def fix_line(line, in_seq):
    l = line.rstrip('\r\n')
    st = l.strip()

    if not st or st.startswith('%%') or st.startswith('flowchart') or st.startswith('sequenceDiagram') or st.startswith('mindmap') or st.startswith('graph'):
        return l

    if in_seq:
        return l

    # Flowchart fixes

    # 1. Strip :::styleClass from decision nodes: NodeID{...}:::style -> NodeID{...}
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*\{[^"\n\}]+\})(:::\w+)', r'\1', l)

    # 2. Sanitize edge labels containing square brackets: |Output: [Retrieve]| -> |"Output: (Retrieve)"|
    def fix_edge_label(m):
        arrow = m.group(1)
        lbl = m.group(2).strip()
        clean = lbl.strip('"' + "'").replace('[', '(').replace(']', ')').replace('"', "'")
        return f'{arrow}"{clean}"|'

    l = re.sub(r'(-->\||->>\||-\.->\||==>\|)([^|\n]+)\|', fix_edge_label, l)

    # 3. Clean node labels with stray quotes/brackets anywhere on line
    def fix_node(m):
        indent = m.group(1)
        nid = m.group(2)
        content = m.group(3)
        style = m.group(4) or ''
        clean = content.replace('"', "'").replace('[', '(').replace(']', ')')
        clean = re.sub(r"'\)$", '', clean)
        clean = re.sub(r"'\]$", '', clean)
        clean = re.sub(r"''$", "'", clean)
        return f'{indent}{nid}["{clean}"]{style}'

    l = re.sub(r'^(\s*)([A-Za-z0-9_\-\.]+)\s*\["(.*)"\](:::\w+)?$', fix_node, l)

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

print(f"Cleaned decision styles, edge labels, and node quotes across {fixed_files} files.")
