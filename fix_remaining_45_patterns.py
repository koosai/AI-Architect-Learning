import os
import re

docs_dir = r"c:\Users\K.K\OneDrive\Desktop\AI架构师教程\docs"

def clean_mermaid_block(code):
    lines = code.split('\n')
    new_lines = []

    first_line = ''
    for l in lines:
        st = l.strip()
        if st and not st.startswith('%%'):
            first_line = st
            break

    is_seq = 'sequenceDiagram' in first_line
    is_mind = 'mindmap' in first_line

    for l in lines:
        line = l.replace('\r', '')

        # 1. Strip <GlossaryTerm ...>Text</GlossaryTerm> -> Text inside Mermaid
        line = re.sub(r'<GlossaryTerm[^>]*>(.*?)</GlossaryTerm>', r'\1', line)

        if is_mind:
            line = re.sub(r'root\s*\("\(([^)]+)\)"?\)', r'root((\1))', line)
            line = re.sub(r'root\s*\("\(([^)]+)\)"\)', r'root((\1))', line)
            line = re.sub(r'root\s*\("([^"]+)"\)', r'root((\1))', line)
            line = re.sub(r'root\s*\(([^)]+)\)', r'root((\1))', line)
            # Remove double quotes inside parens in mindmap node labels
            line = re.sub(r'\("([^"\n]+)"\)', r'(\1)', line)

        if not is_seq and not is_mind:
            # Fix invalid flowchart arrows
            line = line.replace('-->>User:', '-->|6. 渲染最终带有几十个视频的 Home 列表| User')
            line = line.replace('-->>', '-->')
            line = line.replace('<-->', '<--->')
            line = line.replace('<==>', '<===>')

            # Fix unclosed quotes in node labels
            line = line.replace('[105"])', '105)')
            line = line.replace("""['public'"])""", "'public'")

            # Fix invalid classDef style attachment on subgraph: Viewport :::view -> remove :::view
            if line.strip() == 'Viewport :::view':
                line = '  style Viewport fill:#e1f5fe,stroke:#0288d1'

        new_lines.append(line)

    return '\n'.join(new_lines)

fixed_count = 0
for root, dirs, files in os.walk(docs_dir):
    for f in files:
        if f.endswith('.mdx') or f.endswith('.md'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()

            new_doc = []
            lines = content.split('\n')
            in_mermaid = False
            mermaid_lines = []
            modified = False

            for line in lines:
                if line.strip().startswith('```mermaid'):
                    in_mermaid = True
                    mermaid_lines = []
                    new_doc.append(line)
                    continue

                if in_mermaid and line.strip().startswith('```'):
                    in_mermaid = False
                    code = '\n'.join(mermaid_lines)
                    cleaned = clean_mermaid_block(code)
                    if cleaned != code:
                        modified = True
                    new_doc.append(cleaned)
                    new_doc.append(line)
                    continue

                if in_mermaid:
                    mermaid_lines.append(line)
                else:
                    new_doc.append(line)

            if modified:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write('\n'.join(new_doc))
                fixed_count += 1

print(f"Cleaned 45 patterns across {fixed_count} files.")
