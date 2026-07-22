import os
import re

docs_dir = r"c:\Users\K.K\OneDrive\Desktop\AI架构师教程\docs"

# Find all PyRunner blocks in MDX files
def inspect_pyrunner_files():
    fixed_files = []
    for root, dirs, files in os.walk(docs_dir):
        for f in files:
            if f.endswith('.mdx') or f.endswith('.md'):
                filepath = os.path.join(root, f)
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Find PyRunner code blocks: code={`...`}
                pattern = r'(<PyRunner[\s\S]*?code=\{`)([\s\S]*?)(`\}[\s\S]*?/>)'

                def replace_pyrunner(match):
                    prefix = match.group(1)
                    code = match.group(2)
                    suffix = match.group(3)

                    # Fix \n inside single/double quoted string literals in python code
                    # e.g., print("\n--- ...") -> print("\\n--- ...") or print(f"\n...") -> print(f"\\n...")
                    # In JS template string `...`, \n is evaluated as actual newline unless escaped as \\n!
                    
                    # Replace \n inside string quotes
                    # We want \n inside "..." or '...' in Python code to be \\n in the MDX template literal
                    new_code_lines = []
                    for line in code.split('\n'):
                        # Check if line has "\n" or '\n' inside quotes
                        # Example: print("\n---") -> print("\\n---")
                        # But be careful not to double escape if already \\n
                        line_fixed = line
                        # Replace "\n with "\\n
                        line_fixed = re.sub(r'(?<!\\)\\n', r'\\\\n', line_fixed)
                        new_code_lines.append(line_fixed)

                    new_code = '\n'.join(new_code_lines)
                    return prefix + new_code + suffix

                new_content = re.sub(pattern, replace_pyrunner, content)
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    fixed_files.append(filepath)

    print(f"Fixed {len(fixed_files)} files with PyRunner \\n escaping issues:")
    for ff in fixed_files:
        print(" -", os.path.basename(ff))

inspect_pyrunner_files()
