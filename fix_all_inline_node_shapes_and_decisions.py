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

    # Flowchart & Graph fixes (matching anywhere on line)

    # 1. Restore Stadium Shape anywhere: Start("[Text")]) -> Start(["Text"])
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\["\(?([^"\n]+)"?\)?\]\)', r'\1(["\2"])', l)

    # 2. Restore Database Shape anywhere: NodeID["("Text")"] -> NodeID[("Text")]
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\["\("([^"\n]+)"\)"\]', r'\1[("\2")]', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\["\("([^"\n]+)"\)"\]"\)', r'\1[("\2")]', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)"\)', r'\1[("$2")]', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\]"\)', r'\1[("$2")]', l)

    # 3. Restore Circle Shape anywhere: Ring("("Text")")) -> Ring(("Text"))
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)+', r'\1(("$2"))', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)\)"?\)', r'\1(("$2"))', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)', r'\1(("$2"))', l)

    # 4. Decision nodes anywhere: NodeID{Text} -> NodeID{"Clean Text"}
    def fix_decision(m):
        nid = m.group(1)
        inner = m.group(2).strip()
        # If inner is already quoted cleanly with "...", skip
        if inner.startswith('"') and inner.endswith('"') and not inner[1:-1].count('"'):
            return f'{nid}{{{inner}}}'
        clean = inner.replace('"', "'").replace('<br>', '<br/>')
        clean = re.sub(r'\|([^|\n]+)\|', r'abs(\1)', clean)
        return f'{nid}{{"{clean}"}}'

    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\{([^"\n\}]+)\}', fix_decision, l)

    # 5. Fix unquoted/corrupted node strings anywhere: NodeID["Text"]
    def fix_node_string(m):
        nid = m.group(1)
        inner = m.group(2)
        style = m.group(3) or ''
        clean = inner.replace('"', "'").replace('[', '(').replace(']', ')')
        return f'{nid}["{clean}"]{style}'

    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\["([^"\n]+)"\](:::\w+)?', fix_node_string, l)

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

print(f"Cleaned inline node shapes & decision nodes across {fixed_files} files.")
