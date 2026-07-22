import os
import re

docs_dir = r"c:\Users\K.K\OneDrive\Desktop\AI架构师教程\docs"

fixed_files = 0
for root, dirs, files in os.walk(docs_dir):
    for f in files:
        if f.endswith(".mdx") or f.endswith(".md"):
            filepath = os.path.join(root, f)
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

            lines = content.split('\n')
            in_mermaid = False
            in_mindmap = False
            in_seq = False
            new_lines = []
            modified = False

            for line in lines:
                if line.strip().startswith("```mermaid"):
                    in_mermaid = True
                    in_mindmap = False
                    in_seq = False
                    new_lines.append(line)
                    continue
                if in_mermaid and line.strip().startswith("```"):
                    in_mermaid = False
                    in_mindmap = False
                    in_seq = False
                    new_lines.append(line)
                    continue

                if in_mermaid:
                    st = line.strip()
                    if 'mindmap' in st:
                        in_mindmap = True
                    elif 'sequenceDiagram' in st:
                        in_seq = True

                    # 1. Mindmap fixes
                    if in_mindmap:
                        fixed_l = re.sub(r'root\s*\("\(([^)]+)\)"?\)', r'root((\1))', line)
                        fixed_l = re.sub(r'root\s*\("\(([^)]+)\)"\)', r'root((\1))', fixed_l)
                        if fixed_l != line:
                            modified = True
                        new_lines.append(fixed_l)
                        continue

                    # 2. Sequence diagram fixes
                    if in_seq:
                        if st.startswith('subgraph'):
                            indent = re.match(r'^\s*', line).group(0)
                            title = st.replace('subgraph', '').strip('[]"\'').replace('"', "'")
                            fixed_l = f'{indent}box "{title}"'
                            modified = True
                            new_lines.append(fixed_l)
                            continue
                        new_lines.append(line)
                        continue

                    # 3. Flowchart / Graph fixes
                    fixed_l = line
                    # Restore database shapes: [("Text")]
                    fixed_l = fixed_l.replace('["("', '[("').replace('")"]', '")]')
                    # Restore circle shapes: (("Text"))
                    fixed_l = fixed_l.replace('("\\(', '(("').replace('")")', '"))')
                    # Restore stadium shapes: (["Text"])
                    fixed_l = fixed_l.replace('("["', '(["').replace('"]")', '"])')

                    # Convert Note over NodeID: Text -> node in flowchart
                    m_note = re.match(r'^(\s*)Note\s+over\s+([A-Za-z0-9_,\-\.]+)\s*:\s*(.*)$', fixed_l, re.IGNORECASE)
                    if m_note:
                        indent = m_note.group(1)
                        refs = [r.strip() for r in m_note.group(2).split(',')]
                        txt = m_note.group(3).strip().replace('"', "'")
                        first_ref = refs[0].replace('.', '_')
                        note_id = f"Note_{first_ref}"
                        new_lines.append(f'{indent}{note_id}["{txt}"]')
                        for r in refs:
                            new_lines.append(f'{indent}{r} -.-> {note_id}')
                        modified = True
                        continue

                    # Fix subgraph SubID Title (Text) -> subgraph SubID ["Title (Text)"]
                    m_sub = re.match(r'^(\s*)subgraph\s+([A-Za-z0-9_\-\.\u4e00-\u9fa5]+)\s*(.*)$', fixed_l)
                    if m_sub:
                        indent = m_sub.group(1)
                        sub_id = m_sub.group(2)
                        rest = m_sub.group(3).strip()

                        clean_sub_id = re.sub(r'[^\w]', '_', sub_id)
                        if clean_sub_id[0].isdigit():
                            clean_sub_id = f"S_{clean_sub_id}"

                        if rest:
                            clean_title = rest.strip('[]"\'').replace('"', "'")
                            fixed_l = f'{indent}subgraph {clean_sub_id} ["{clean_title}"]'
                        else:
                            if clean_sub_id != sub_id:
                                fixed_l = f'{indent}subgraph {clean_sub_id} ["{sub_id}"]'
                            else:
                                fixed_l = f'{indent}subgraph {clean_sub_id}'

                    # Fix node IDs starting with digits e.g. 12306 -> N_12306
                    fixed_l = re.sub(r'\b([0-9][A-Za-z0-9_\-\.]*)\s*(\[|\()', r'N_\1\2', fixed_l)

                    # Edge labels -->|Text| -> -->|"Text"|
                    def clean_edge(m):
                        arrow = m.group(1)
                        lbl = m.group(2).strip().strip('"\'').replace('"', "'")
                        return f'{arrow}"{lbl}"|'

                    fixed_l = re.sub(r'(-->\||->>\||-\.->\||==>\|)([^|\n]+)\|', clean_edge, fixed_l)

                    if fixed_l != line:
                        modified = True
                    new_lines.append(fixed_l)
                else:
                    new_lines.append(line)

            if modified:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write('\n'.join(new_lines))
                fixed_files += 1

print(f"Applied safe line-by-line fixes across {fixed_files} files.")
