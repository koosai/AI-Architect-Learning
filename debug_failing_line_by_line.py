import json

with open('mermaid_errors.json', 'r', encoding='utf-8') as f:
    errs = json.load(f)

for item in errs[:10]:
    filename = item['file'].split('/')[-1]
    print(f"=== {filename} (Line {item['startLine']}) ===")
    print("Error:", item['error'].split('\n')[0])
    lines = item['code'].split('\n')
    for idx, l in enumerate(lines):
        print(f"  {idx+1:2d}: {l}")
    print()
