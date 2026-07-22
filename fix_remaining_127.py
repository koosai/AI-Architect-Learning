import os
import re

docs_dir = r"c:\Users\K.K\OneDrive\Desktop\AI架构师教程\docs"

def fix_line(line):
    l = line.rstrip('\r\n')

    # 1. Invalid arrow syntax: -.-x| or -->x| or -.-x
    l = re.sub(r'-\.-\s*x\|', '-.->|', l)
    l = re.sub(r'-->\s*x\|', '-->|', l)
    l = re.sub(r'-\.-\s*x\s', '-.-> ', l)

    # 2. Circle shape: Name(("Text")) from Name("("Text"))) or Name("("Text"))
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)\)"?\)', r'\1(("\2"))', l)
    l = re.sub(r'(\b[A-Za-z0-9_\-\.]+\s*)\("\("([^"\n]+)"\)\)', r'\1(("\2"))', l)

    # 3. Inner quotes inside NodeID["..."]
    # E.g. tokens = min("capacity, ...") -> tokens = min('capacity', ...)
    def clean_inner_quotes(m):
        nid = m.group(1)
        bopen = m.group(2)
        inner = m.group(3)
        bclose = m.group(4)
        style = m.group(5) or ""

        # Replace internal quotes and brackets
        clean = inner.replace('"', "'")
        clean = clean.replace('[', '(').replace(']', ')')
        return f'{nid}{bopen}"{clean}"{bclose}{style}'

    l = re.sub(r'\b([A-Za-z0-9_\-\.]+)\s*(\[|\()([^\]\)\n]+)(\]||\))(:::\w+)?', clean_inner_quotes, l)

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
                    fixed_l = fix_line(line)
                    if fixed_l != line:
                        modified = True
                    new_lines.append(fixed_l)
                else:
                    new_lines.append(line)

            if modified:
                with open(filepath, "w", encoding="utf-8") as file:
                    file.writelines(new_lines)
                fixed_files += 1

print(f"Fixed remaining arrow/circle/quote issues across {fixed_files} files.")
