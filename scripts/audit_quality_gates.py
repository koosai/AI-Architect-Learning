import os
import re
import sys

docs_dir = r"c:\Users\K.K\OneDrive\Desktop\AI架构师教程\docs"
output_file = r"C:\Users\K.K\.gemini\antigravity-ide\brain\6584009d-4c1e-4be5-b3ef-82b38b145faa\quality_gate_audit.md"

mermaid_pattern = re.compile(r'```mermaid', re.IGNORECASE)

interactive_components = [
    'TradeoffExplorer', 'SystemSimulator', 'StepFlow', 
    'PercentileLab', 'LatencyNumbers', 'FailureLab', 
    'CapacityEstimator', 'CompareSlider', 'ArchLayers', 
    'MindMap', 'ArchitectureEvolution', 'CacheSimulator'
]

experiment_components = ['PyRunner', 'GuidedExercise']

def count_quiz_questions(content):
    # Match pattern: q: '...' or q: "..." or q: `...`
    # Also handles potential spacing
    return len(re.findall(r'\bq\s*:\s*[\'"`]', content))

def analyze_file(filepath, relative_path):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(filepath, 'r', encoding='gb18030', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filepath} with fallback: {e}")
            return None
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None
    
    mermaid_count = len(mermaid_pattern.findall(content))
    
    interactives = {}
    total_interactives = 0
    for comp in interactive_components:
        count = len(re.findall(rf'<{comp}\b', content))
        if count > 0:
            interactives[comp] = count
            total_interactives += count
            
    experiments = {}
    total_experiments = 0
    for comp in experiment_components:
        count = len(re.findall(rf'<{comp}\b', content))
        if count > 0:
            experiments[comp] = count
            total_experiments += count
            
    quiz_count = len(re.findall(r'<QuizCard\b', content))
    quiz_questions = count_quiz_questions(content)
    
    glossary_count = len(re.findall(r'<GlossaryTerm\b', content))
    research_note_count = len(re.findall(r'<ResearchNote\b', content))
    
    mermaid_ok = mermaid_count >= 3
    interactive_ok = total_interactives >= 1
    quiz_ok = quiz_questions >= 3
    
    # We should exclude index or overview or start/component-gallery pages from strict gates since they are not standard chapters.
    is_meta_page = any(x in relative_path for x in [
        'overview.md', 'overview.mdx', 'index.md', 'index.mdx', 
        'glossary.mdx', 'component-gallery', '00-start', 'projects',
        'capstone-brief'
    ])
    
    fully_compliant = is_meta_page or (mermaid_ok and interactive_ok and quiz_ok)
    
    return {
        'relative_path': relative_path.replace('\\', '/'),
        'mermaid_count': mermaid_count,
        'total_interactives': total_interactives,
        'total_experiments': total_experiments,
        'quiz_questions': quiz_questions,
        'glossary_count': glossary_count,
        'research_note_count': research_note_count,
        'mermaid_ok': mermaid_ok,
        'interactive_ok': interactive_ok,
        'quiz_ok': quiz_ok,
        'fully_compliant': fully_compliant,
        'is_meta_page': is_meta_page,
        'interactives_detail': ", ".join(f"{k}({v})" for k, v in interactives.items()) or "None",
        'experiments_detail': ", ".join(f"{k}({v})" for k, v in experiments.items()) or "None"
    }

def main():
    results = []
    
    for root, dirs, files in os.walk(docs_dir):
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        if 'build' in dirs:
            dirs.remove('build')
            
        for file in files:
            if file.endswith(('.md', '.mdx')):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, docs_dir)
                res = analyze_file(full_path, rel_path)
                if res:
                    results.append(res)
                    
    # Sort results by path
    results.sort(key=lambda x: x['relative_path'])
    
    # Generate report
    total_files = len(results)
    non_compliant_chapters = [r for r in results if not r['fully_compliant'] and not r['is_meta_page']]
    
    report = []
    report.append("# Quality Gate Audit Report\n")
    report.append(f"**Total audited files:** {total_files}\n")
    report.append(f"**Fully compliant chapters:** {total_files - len(non_compliant_chapters)} / {total_files}\n")
    report.append(f"**Compliance rate (excluding meta/gallery pages):** {(1.0 - len(non_compliant_chapters)/total_files)*100:.2f}%\n")
    
    if non_compliant_chapters:
        report.append("## Non-Compliant Chapters\n")
        report.append(r"The following chapters do not meet the quality gate criteria (Mermaid $\ge$ 3, Interactive $\ge$ 1, Quiz questions $\ge$ 3):\n")
        report.append("| File Path | Mermaid Count | Interactives | Quiz Questions | Deficiencies |\n")
        report.append("|---|---|---|---|---|\n")
        for r in non_compliant_chapters:
            defs = []
            if not r['mermaid_ok']:
                defs.append(f"Mermaid ({r['mermaid_count']}/3)")
            if not r['interactive_ok']:
                defs.append(f"Interactive ({r['total_interactives']}/1)")
            if not r['quiz_ok']:
                defs.append(f"Quiz ({r['quiz_questions']}/3)")
            
            report.append(f"| {r['relative_path']} | {r['mermaid_count']} | {r['interactives_detail']} | {r['quiz_questions']} | {', '.join(defs)} |\n")
        report.append("\n")
        
    report.append("## All Audited Pages Details\n")
    report.append("| File Path | Mermaid | Interactives | Experiments | Quiz Qs | Glossary | ResearchNote | Status |\n")
    report.append("|---|---|---|---|---|---|---|---|\n")
    
    for r in results:
        status = "✅ Compliant" if r['fully_compliant'] else "❌ Non-compliant"
        if r['is_meta_page']:
            status = "ℹ️ Meta Page"
        report.append(f"| {r['relative_path']} | {r['mermaid_ok'] and '✅' or '❌'} ({r['mermaid_count']}) | {r['interactives_detail']} | {r['experiments_detail']} | {r['quiz_ok'] and '✅' or '❌'} ({r['quiz_questions']}) | {r['glossary_count']} | {r['research_note_count']} | {status} |\n")
        
    # Write report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(report)
        
    print(f"Audit completed. Report written to: {output_file}")
    print(f"Total non-compliant chapters: {len(non_compliant_chapters)}")

if __name__ == '__main__':
    main()
