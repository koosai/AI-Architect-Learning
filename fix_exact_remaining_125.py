import os
import re

docs_dir = r"c:\Users\K.K\OneDrive\Desktop\AI架构师教程\docs"

def clean_mermaid_line(line):
    l = line.rstrip('\r\n')

    # 1. Circle shape: Name(("Text"))
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)\)"?\)', r'\1(("\2"))', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)', r'\1(("\2"))', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)\)', r'\1(("\2"))', l)

    # 2. Database shape: NodeID[("Text")]
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\["\("([^"\n]+)"\)"\]', r'\1[("\2")]', l)

    # 3. Fix inner double quotes and stray closing quotes inside NodeID["..."]
    def fix_node_string(m):
        nid = m.group(1)
        bopen = m.group(2) # [ or (
        content = m.group(3)
        bclose = m.group(4) # ] or )
        style = m.group(5) or ""

        # Remove outer quotes if present
        clean = content.strip()
        while (clean.startswith('"') and clean.endswith('"')) or (clean.startswith("'") and clean.endswith("'")):
            clean = clean[1:-1].strip()

        # Remove stray "] or "] at end
        clean = re.sub(r'"\]$', '', clean)
        clean = re.sub(r'"]', ')', clean)
        clean = re.sub(r'\[', '(', clean)

        # Replace any remaining double quotes inside content with single quotes
        clean = clean.replace('"', "'")

        return f'{nid}{bopen}"{clean}"{bclose}{style}'

    l = re.sub(r'\b([A-Za-z0-9_\-\.]+)\s*(\[|\()([^\]\)\n]+)(\]||\))(:::\w+)?', fix_node_string, l)

    # 4. Fix Edge Labels: -->|Text| -> -->|"Text"|
    def fix_edge_string(m):
        arrow = m.group(1)
        lbl = m.group(2).strip()
        while (lbl.startswith('"') and lbl.endsWith('"')) or (lbl.startsWith("'") and lbl.endsWith("'")):
            lbl = lbl[1:-1].strip()
        lbl = lbl.replace('"', "'")
        return f'{arrow}"{lbl}"|'

    # 5. Fix subgraph titles: subgraph SubID ["Title"]
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
            l = f'{indent}subgraph {clean_sub_id} ["{clean_title}"]'
        else:
            if clean_sub_id != sub_id:
                l = f'{indent}subgraph {clean_sub_id} ["{sub_id}"]'
            else:
                l = f'{indent}subgraph {clean_sub_id}'

    return l

fixed_files = 0
for root, dirs, files in os.walk(docs_dir):
    for f in files:
        if f.endswith(".mdx") or f.endswith(".md"):
            filepath = os.path.join(root, f)
            with open(filepath, "r", encoding="utf-8") as file:
                lines = file.readlines()

            in_mermaid = False
            new_lines = []
            modified = False

            for line in lines:
                if line.strip().startswith("```mermaid"):
                    in_mermaid = True
                    new_lines.append(line)
                    continue
                if in_mermaid and line.strip().startswith("```"):
                    in_mermaid = False
                    new_lines.append(line)
                    continue
                if in_mermaid:
                    fixed_l = clean_mermaid_line(line)
                    if fixed_l != line:
                        modified = True
                    new_lines.append(fixed_l)
                else:
                    new_lines.append(line)

            if modified:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.writelines(new_lines)
                fixed_files += 1

print(f"Fixed remaining shape/quote corruptions across {fixed_files} files.")
