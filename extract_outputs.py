import os
import json
import re

directories = [
    r"c:\Users\gauri\Desktop\Machine-Learning-Projects\Supervised Learning Projects",
    r"c:\Users\gauri\Desktop\Machine-Learning-Projects\Unsupervised Learning Projects"
]

def extract_meaningful_output(cell_text):
    # Try to grab lines that contain key metrics
    lines = cell_text.split('\n')
    meaningful_lines = []
    keywords = ['accuracy', 'r2', 'score', 'rmse', 'mae', 'precision', 'recall', 'f1', 'cluster', 'recommend', 'silhouette']
    for line in lines:
        if any(kw in line.lower() for kw in keywords):
            meaningful_lines.append(line.strip())
    
    # If no keywords found, but there's output, just return the last 3 lines
    if not meaningful_lines and len(lines) > 0:
        meaningful_lines = [l.strip() for l in lines[-3:] if l.strip()]
        
    # limit to 10 lines
    return "\n".join(meaningful_lines[-10:])

markdown_output = "# Final Model Outputs\n\n"

for dir_path in directories:
    dir_name = os.path.basename(dir_path)
    markdown_output += f"## {dir_name}\n\n"
    
    for folder in sorted(os.listdir(dir_path)):
        folder_path = os.path.join(dir_path, folder)
        if not os.path.isdir(folder_path):
            continue
            
        markdown_output += f"### {folder}\n```text\n"
        
        found_output = False
        for root, _, files in os.walk(folder_path):
            for f in files:
                if f.endswith('.ipynb'):
                    path = os.path.join(root, f)
                    try:
                        with open(path, 'r', encoding='utf-8') as file:
                            nb = json.load(file)
                            
                        # Look at the last 15 cells for outputs
                        for cell in nb.get('cells', [])[-15:]:
                            cell_text = ""
                            for output in cell.get('outputs', []):
                                if 'text' in output:
                                    cell_text += "".join(output['text'])
                                if 'data' in output and 'text/plain' in output['data']:
                                    cell_text += "".join(output['data']['text/plain'])
                            
                            if cell_text.strip():
                                extracted = extract_meaningful_output(cell_text)
                                if extracted:
                                    markdown_output += extracted + "\n...\n"
                                    found_output = True
                    except Exception as e:
                        print(f"Error {path}")
                        
        if not found_output:
            markdown_output += "No obvious text outputs found in the last cells of the notebook.\n"
        markdown_output += "```\n\n"

with open(r"c:\Users\gauri\Desktop\Machine-Learning-Projects\model_outputs.md", "w", encoding='utf-8') as f:
    f.write(markdown_output)

print("Extraction complete. Output written to model_outputs.md")
