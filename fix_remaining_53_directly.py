import os
import re

docs_dir = r"c:\Users\K.K\OneDrive\Desktop\AI架构师教程\docs"

def fix_content(content):
    # 1. Fix flowchart Note over
    def replace_flowchart_note(m):
        refs = m.group(1).split(',')
        refs = [r.strip() for r in refs]
        txt = m.group(2).strip().replace('"', "'").replace('[', '(').replace(']', ')')
        note_id = f"Note_{refs[0].replace('.', '_')}"
        res = [f'{note_id}["{txt}"]']
        for r in refs:
            res.append(f'{r} -.-> {note_id}')
        return '\n'.join(res)

    lines = content.split('\n')
    in_mermaid = False
    in_seq = False
    out_lines = []

    for line in lines:
        st = line.strip()
        if st.startswith('```mermaid'):
            in_mermaid = True
            in_seq = False
            out_lines.append(line)
            continue
        if in_mermaid and st.startswith('```'):
            in_mermaid = False
            in_seq = False
            out_lines.append(line)
            continue

        if in_mermaid:
            if 'sequenceDiagram' in line:
                in_seq = True

            l = line

            if not in_seq:
                # Flowchart Note over
                m_note = re.match(r'^\s*Note\s+over\s+([A-Za-z0-9_,\-\.]+)\s*:\s*(.*)$', l, re.IGNORECASE)
                if m_note:
                    l = replace_flowchart_note(m_note)

                # Fix mindmap root
                l = re.sub(r'root\s*\("\(([^)]+)\)"?\)', r'root((\1))', l)
                l = re.sub(r'root\s*\("\(([^)]+)\)"\)', r'root((\1))', l)
                l = re.sub(r'root\s*\("([^"]+)"\)', r'root((\1))', l)
                l = re.sub(r'root\s*\(([^)]+)\)', r'root((\1))', l)

                # Fix arrows
                l = l.replace('<-->', '<--->')
                l = l.replace('<==>', '<===>')

                # Fix database shape
                l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\["\("([^"\n]+)"\)"\]', r'\1[("\2")]', l)
                l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\["\("([^"\n]+)"\]"\)\]', r'\1[("\2")]', l)

                # Fix circle shape
                l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)+', r'\1(("\2"))', l)
                l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)\)"?\)', r'\1(("\2"))', l)
                l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)', r'\1(("\2"))', l)
                l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\(([^"\n]+)\)"\)+', r'\1(("$2"))', l)
                l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\(([^"\n]+)\)"\)', r'\1(("\2"))', l)

                # Clean unclosed quotes inside parens/brackets in node text
                l = l.replace("['public'\"])", "'public'")
                l = l.replace(')""}', ')"}')

            out_lines.append(l)
        else:
            out_lines.append(line)

    return '\n'.join(out_lines)

count = 0
for root, dirs, files in os.walk(docs_dir):
    for f in files:
        if f.endswith('.mdx') or f.endswith('.md'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            fixed = fix_content(content)
            if fixed != content:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(fixed)
                count += 1

print(f"Fixed remaining 53 issues across {count} files.")
