import os
import re

docs_dir = r"c:\Users\K.K\OneDrive\Desktop\AI架构师教程\docs"

def fix_diagram_text(line, in_seq):
    l = line.rstrip('\r\n')
    st = l.strip()

    # 1. Sequence Diagram Subgraph Fix: subgraph SubID ["Title"] -> box "Title"
    if in_seq:
        if st.startswith('subgraph'):
            indent = re.match(r'^\s*', l).group(0)
            m = re.match(r'^\s*subgraph\s+(?:[A-Za-z0-9_\-\.]+\s*)?\[?"?(.*?)"?\]?$', l)
            if m:
                title = m.group(1).replace('"', "'").strip('[]')
                return f'{indent}box "{title}"'
            else:
                title = st.replace('subgraph', '').strip('[]"\'')
                return f'{indent}box "{title}"'

    # 2. Fix trailing double closing parens: ...branche")") -> ...branches)"]
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*\["[^"\n]+)"\)\)', r'\1)"]', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*\["[^"\n]+)"\)', r'\1"]', l)

    # 3. Restore Circle Shape: Name(("Text"))
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)+', r'\1(("\2"))', l)

    # 4. Clean stray inner quotes in node labels: min("capacity -> min('capacity
    def clean_inner_node(m):
        nid = m.group(1)
        content = m.group(2)
        style = m.group(3) or ""

        # Replace double quotes inside content with single quotes
        clean = content.replace('"', "'").replace('[', '(').replace(']', ')')
        return f'{nid}["{clean}"]{style}'

    l = re.sub(r'\b([A-Za-z0-9_\-\.]+)\s*\["([^"\n]+)"\](:::\w+)?', clean_inner_node, l)

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
                    fixed = fix_diagram_text(line, in_seq)
                    if fixed != line:
                        modified = True
                    new_lines.append(fixed)
                else:
                    new_lines.append(line)

            if modified:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.writelines(new_lines)
                fixed_files += 1

print(f"Repaired sequence subgraphs & node quotes across {fixed_files} files.")
