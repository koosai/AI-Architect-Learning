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
            raw = re.sub(r'^\s*(?:subgraph|box)\s*(?:[A-Za-z0-9_\-\.]+\s*)?', '', l).strip()
            title = raw.strip('[]"\'').replace('->', '→').replace('"', "'")
            return f'{indent}box "{title}"'
        elif st.startswith('Note'):
            return l.replace('->', '→').replace('"', "'")
        elif ':' in l:
            parts = l.split(':')
            prefix = parts[0]
            msg = ':'.join(parts[1:]).strip().replace('"', "'").replace('[', '(').replace(']', ')')
            return f'{prefix}: {msg}'
        return l

    # Flowchart fixes

    # 1. Replace invalid bidirectional arrow <--> with <---> in flowcharts
    l = l.replace('<-->', '<--->')

    # 2. Restore Stadium Shape: Start("[Text")]) or Start("[Text]") anywhere
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\["\(?([^"\n]+)"?\)?\]\)', r'\1(["\2"])', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\["([^"\n]+)"\]\)', r'\1(["\2"])', l)

    # 3. Restore Database Shape: NodeID["("Text")"] / NodeID["("Text"]")] anywhere
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\["\("([^"\n]+)"\)"\]', r'\1[("$2")]', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\["\("([^"\n]+)"\]"\)\]', r'\1[("$2")]', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\["\("([^"\n]+)"\)"\]"\)', r'\1[("$2")]', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)"\)', r'\1[("$2")]', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\]"\)', r'\1[("$2")]', l)

    # 4. Restore Circle Shape: Ring["(("Text"))"] or Ring("("Text")")) -> Ring(("Text"))
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\["\(\("([^"\n]+)"\)\)"\]', r'\1(("\2"))', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)+', r'\1(("$2"))', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)\)"?\)', r'\1(("$2"))', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)', r'\1(("$2"))', l)

    # 5. Quote & Sanitize Decision Nodes NodeID{Text} -> NodeID{"Clean Text"} (strip :::style from decision nodes)
    def fix_decision(m):
        nid = m.group(1)
        inner = m.group(2).strip()
        clean = inner.replace('""', '"').strip('"')
        clean = clean.replace('|', '').replace('"', "'")
        return f'{nid}{{"{clean}"}}'

    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\{([^"\n\}]+)\}(?:::\w+)?', fix_decision, l)

    # 6. Subgraph title quotes: subgraph SubID ["Title"]
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
        else:
            if clean_sub_id != sub_id:
                return f'{indent}subgraph {clean_sub_id} ["{sub_id}"]'
            return f'{indent}subgraph {clean_sub_id}'

    # 7. Edge label sanitization
    def fix_edge_label(m):
        arrow = m.group(1)
        lbl = m.group(2).strip()
        clean = lbl.strip('"' + "'").replace('[', '(').replace(']', ')').replace('"', "'")
        return f'{arrow}"{clean}"|'

    l = re.sub(r'(-->\||->>\||-\.->\||==>\|)([^|\n]+)\|', fix_edge_label, l)

    # 8. Clean inner quotes & parens in node labels anywhere on line: NodeID["Text"]
    def fix_node_string(m):
        p1 = m.group(1)
        inner = m.group(2)
        p3 = m.group(3)
        style = m.group(4) or ''
        clean = inner.replace('"', "'").replace('[', '(').replace(']', ')')
        clean = re.sub(r"'\)$", '', clean)
        clean = re.sub(r"'\]$", '', clean)
        clean = re.sub(r"''$", "'", clean)
        return f'{p1}{clean}{p3}{style}'

    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*\[")([^"\n]+)("\])(:::\w+)?', fix_node_string, l)

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

print(f"Applied precision AST fixes across {fixed_files} files.")
