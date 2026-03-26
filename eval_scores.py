import os
import json
import re

supervised_dir = r"c:\Users\gauri\Desktop\Machine-Learning-Projects\Supervised Learning Projects"

project_scores = {}

# Patterns that might indicate a score.
# e.g., "Accuracy: 0.95", "R2 Score: 0.88", "accuracy score is 0.92"
score_patterns = [
    r"accuracy.*?(\d+\.\d+)",
    r"r2.*?(\d+\.\d+)",
    r"score.*?(\d+\.\d+)",
    r"precision.*?(\d+\.\d+)",
    r"recall.*?(\d+\.\d+)",
    r"f1.*?(\d+\.\d+)",
]

def extract_best_score(text):
    best = 0.0
    text = text.lower()
    for pattern in score_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                val = float(match)
                if val > 1.0 and val <= 100.0:
                    val = val / 100.0
                if val <= 1.0 and val > best:
                    best = val
            except:
                pass
    return best

for root, dirs, files in os.walk(supervised_dir):
    for f in files:
        if f.endswith('.ipynb'):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    nb = json.load(file)
                    
                text_content = ""
                for cell in nb.get('cells', []):
                    # Check outputs
                    for output in cell.get('outputs', []):
                        if 'text' in output:
                            text_content += "".join(output['text'])
                        if 'data' in output and 'text/plain' in output['data']:
                            text_content += "".join(output['data']['text/plain'])
                    # Check source for print statements with scores
                    if 'source' in cell:
                        text_content += "".join(cell['source'])
                
                score = extract_best_score(text_content)
                proj_name = os.path.basename(os.path.dirname(path))
                if proj_name not in project_scores or score > project_scores[proj_name]:
                    project_scores[proj_name] = score
            except Exception as e:
                print(f"Error reading {f}: {e}")

# Sort projects by score descending
sorted_projects = sorted(project_scores.items(), key=lambda x: x[1], reverse=True)

print("--- Supervised Projects Scores ---")
for proj, score in sorted_projects:
    print(f"{proj}: {score:.4f}")

