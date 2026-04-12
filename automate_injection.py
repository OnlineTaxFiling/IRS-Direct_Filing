import os
import json
from github import Github # pip install PyGithub

# --- CONFIGURATION ---
GITHUB_TOKEN = 'your_personal_access_token'
REPO_NAME = 'OnlineTaxFiling/IRS-Direct_Filing'
KEYWORD_FILE = 'keywords.json'

def get_next_keywords(count=10):
    with open(KEYWORD_FILE, 'r') as f:
        data = json.load(f)
    
    selected = data['remaining'][:count]
    data['remaining'] = data['remaining'][count:]
    data['used'].extend(selected)
    
    with open(KEYWORD_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    return selected

def inject_content(html_content, new_block):
    # Targets the specific injection point we set in the HTML
    marker = ''
    return html_content.replace(marker, f"{new_block}\n{marker}")

def update_github(repo_name, file_path, new_html):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo_name)
    contents = repo.get_contents(file_path)
    
    repo.update_file(
        contents.path, 
        "Daily Authority Injection: Adding 500+ words of depth", 
        new_html, 
        contents.sha
    )

# --- EXECUTION ---
# 1. Get Keywords
keywords = get_next_keywords(10)

# 2. (Self-Correction/Instruction) 
# You would send these keywords to the Content AI here to generate 
# the 500-word <div> block using the "Secret Logic" parameters.

new_div_block = f"""
<section>
    <h3>Deep Dive: {keywords[0]} and {keywords[1]}</h3>
    <p>New evidence suggests that for the 2026 tax season, {keywords[0]} is becoming 
    a primary focus for IRS automated audits. Expert filers recommend...</p>
</section>
"""

# 3. Read current local file, inject, and push
with open('index.html', 'r') as f:
    current_html = f.read()

updated_html = inject_content(current_html, new_div_block)
update_github(REPO_NAME, 'index.html', updated_html)
