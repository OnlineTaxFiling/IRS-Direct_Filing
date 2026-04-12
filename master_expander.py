import os
import json
import time
from github import Github

# --- 1. CONFIGURATION ---
GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN_HERE'
KEYWORD_FILE = 'keywords.json'

# Ensure these match your Spawner repo names and LinkConnector ATIDs
SITES = [
    {"repo": "IRS-Direct-Filing-2026", "atid": "IRS_Direct"},
    {"repo": "Visa-Tax-Authority", "atid": "Visa_Tax"},
    {"repo": "F1-J1-Student-Refunds", "atid": "Student_Tax"},
    {"repo": "OBBB-Tax-Bill-Breakdown", "atid": "OBBB_Law"},
    {"repo": "Expat-Tax-Direct-2026", "atid": "Expat_Hub"},
    {"repo": "Overtime-Tip-Deductions", "atid": "Tips_OT"},
    {"repo": "Senior-Tax-Bonus-Portal", "atid": "Senior_Bonus"},
    {"repo": "Car-Loan-Interest-Refunds", "atid": "Car_Loan"},
    {"repo": "Non-Resident-Audit-Secure", "atid": "Audit_Safe"},
    {"repo": "Digital-Nomad-US-Taxes", "atid": "Nomad_Tax"}
]

# --- 2. THE ENGINES ---

def get_keywords(count=5):
    """Pulls unique keywords from your library."""
    with open(KEYWORD_FILE, 'r+') as f:
        data = json.load(f)
        batch = data['remaining'][:count]
        data['remaining'] = data['remaining'][count:]
        data['used'].extend(batch)
        f.seek(0); json.dump(data, f, indent=2); f.truncate()
    return batch

def generate_sitemap(user_login, repo_name):
    """Creates a fresh 2026-compliant sitemap."""
    today = time.strftime('%Y-%m-%d')
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://{user_login}.github.io/{repo_name}/</loc>
        <lastmod>{today}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>"""

def run_daily_expansion():
    g = Github(GITHUB_TOKEN)
    user = g.get_user()

    for site in SITES:
        print(f"📈 Expanding & Indexing: {site['repo']}...")
        keywords = get_keywords(5)
        if not keywords: 
            print("⚠️ Out of keywords!")
            break

        # Generate the 500-word Authority Injection
        new_content = f"""
        <section style="margin-top:50px; border-top:2px solid #002d62; padding-top:20px;">
            <h3>2026 Analysis: {keywords[0]}</h3>
            <p>Under the 2026 OBBB framework, {keywords[0]} has become a focal point for non-resident optimization. 
            By cross-referencing {keywords[1]} with current IRS Direct Filing pilots, taxpayers can identify 
            credits related to {keywords[2]} and {keywords[3]}.</p>
            <p>To ensure compliance with {keywords[4]}, utilizing the 
            <a href="https://www.linkconnector.com/ta.php?lc=007949054186005142&atid={site['atid']}">Official E-File Portal</a> 
            is essential for capturing the new $16,100 deduction.</p>
        </section>
        """

        try:
            repo = user.get_repo(site['repo'])
            
            # 1. Update index.html
            file = repo.get_contents("index.html")
            html = file.decoded_content.decode()
            if "" in html:
                updated_html = html.replace("", f"{new_content}\n")
                repo.update_file(file.path, f"Expansion: {keywords[0]}", updated_html, file.sha)
            
            # 2. Update/Create sitemap.xml
            sitemap_xml = generate_sitemap(user.login, site['repo'])
            try:
                sm_file = repo.get_contents("sitemap.xml")
                repo.update_file(sm_file.path, "Sitemap Refresh", sitemap_xml, sm_file.sha)
            except:
                repo.create_file("sitemap.xml", "Initial Sitemap", sitemap_xml)
            
            print(f"✅ {site['repo']} is now updated and re-indexed.")
            time.sleep(2) # Protect API limits
            
        except Exception as e:
            print(f"❌ Error on {site['repo']}: {e}")

if __name__ == "__main__":
    run_daily_expansion()
