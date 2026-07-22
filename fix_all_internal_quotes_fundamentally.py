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
        return l

    # Flowchart diagram fixes

    # 1. Circle shape: Name("("Text")")) -> Name(("Text"))
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)+', r'\1(("\2"))', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)\)"?\)', r'\1(("\2"))', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)', r'\1(("\2"))', l)

    # 2. Database shape: NodeID[("Text")]
    l = re.sub(r'\b([A-Za-z0-9_\-\.]+)\s*\["\("([^"\n]+)"\)"\]', r'\1[("$2")]', l)

    # 3. Clean node string labels: NodeID["..."]
    def clean_node_match(m):
        nid = m.group(1)
        content = m.group(2)
        style = m.group(3) or ''

        # Strip any inner double quotes
        clean = content.replace('"', "'")
        # Replace unescaped inner brackets with parens
        clean = clean.replace('[', '(').replace(']', ')')
        return f'{nid}["{clean}"]{style}'

    # Match NodeID["..."] where content can contain anything before closing "]
    l = re.sub(r'\b([A-Za-z0-9_\-\.]+)\s*\["([^"\n]+)"\](:::\w+)?', clean_node_match, l)

    # Clean stray duplicate closing quotes at end of node labels like "]"]
    l = re.sub(r'"\]"\]$', '"]', l)
    l = re.sub(r'"\]"\)$', '"]', l)

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

print(f"Cleaned internal quotes & shapes across {fixed_files} files.")
