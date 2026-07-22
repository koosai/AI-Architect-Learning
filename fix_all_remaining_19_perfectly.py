import os
import re

docs_dir = r"c:\Users\K.K\OneDrive\Desktop\AI架构师教程\docs"

def fix_content(content):
    lines = content.split('\n')
    new_doc = []
    in_mermaid = False
    is_seq = False
    is_mind = False

    for line in lines:
        st = line.strip()
        if st.startswith('```mermaid'):
            in_mermaid = True
            is_seq = False
            is_mind = False
            new_doc.append(line)
            continue

        if in_mermaid and st.startswith('```'):
            in_mermaid = False
            is_seq = False
            is_mind = False
            new_doc.append(line)
            continue

        if in_mermaid:
            if 'sequenceDiagram' in st:
                is_seq = True
            if 'mindmap' in st:
                is_mind = True

            l = line

            # 1. Flowchart arrow fixes
            if not is_seq and not is_mind:
                # Fix -.- "|label|" -> -.->|"label"|
                l = re.sub(r'([A-Za-z0-9_\-\.]+)\s*-\.-\s*"\|([^|]+)\|"\s*([A-Za-z0-9_\-\.]+)', r'\1 -.->|"\2"| \3', l)

                # Fix <--|label| -> -->|label|
                l = re.sub(r'([A-Za-z0-9_\-\.]+)\s*<--\|([^|]+)\|\s*([A-Za-z0-9_\-\.]+)', r'\3 -->|"\2"| \1', l)
                l = re.sub(r'([A-Za-z0-9_\-\.]+)\s*<==\|([^|]+)\|\s*([A-Za-z0-9_\-\.]+)', r'\3 ==>|"\2"| \1', l)

                # Fix double labels --"lbl1"-->|lbl2| -> -->|"lbl1: lbl2"|
                l = re.sub(r'--"([^"]+)"-->\|([^|]+)\|', r'-->|"\1: \2"|', l)
                l = re.sub(r'-\.-"([^"]+)"->\|([^|]+)\|', r'-.->|"\1: \2"|', l)
                l = re.sub(r'-\.-"([^"]+)"-\.->\|([^|]+)\|', r'-.->|"\1: \2"|', l)

                # Fix alt/else in flowchart
                if st.startswith('alt ') or st.startswith('else ') or st == 'end':
                    l = f"%% {st}"

                # Fix [Del"]) unclosed brackets
                l = l.replace('[Del"])', ' (Del)')

                # Fix unclosed parens in node label
                l = l.replace('(用户 ACL: [' + "'public'\"])", "(用户 ACL: 'public')")
                l = l.replace('("W + R = 4 > 3")', "'W + R = 4 > 3'")

            # 2. Sequence diagram fixes
            if is_seq:
                l = l.replace('-.>>', '-->>')
                l = l.replace('-.->', '-->')

            new_doc.append(l)
        else:
            new_doc.append(line)

    return '\n'.join(new_doc)

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

print(f"Fixed remaining 19 patterns across {count} files.")
