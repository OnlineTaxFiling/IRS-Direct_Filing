import os
import json
import time
from github import Github

# --- 1. CONFIGURATION ---
# Uses Environment Variable for security in GitHub Actions
GITHUB_TOKEN = os.getenv('CHAMELEON_TOKEN') 
KEYWORD_FILE = 'keywords.json'

# Match these to your Spawner names
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

# --- 2. THE ENGINE FUNCTIONS ---

def get_keywords(count=5):
    """Pulls keywords and updates the JSON file to track 'used' terms."""
    if not os.path.exists(KEYWORD_FILE):
        return []
    with open(KEYWORD_FILE, 'r+') as f:
        data = json.load(f)
        batch = data['remaining'][:count]
        data['remaining'] = data['remaining'][count:]
        data['used'].extend(batch)
        f.seek(0); json.dump(data, f, indent=2); f.truncate()
    return batch

def generate_sitemap(user_login, repo_name):
    """Pings crawlers with a fresh date stamp."""
    today = time.strftime('%Y-%m-%d')
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>https://{user_login}.github.io/{repo_name}/</loc><lastmod>{today}</lastmod><priority>1.0</priority></url>
</urlset>"""

def build_content(kws, atid):
    """Generates the technical authority block for 2026."""
    url = f"https://www.linkconnector.com/ta.php?lc=007949054186005142&atid={atid}"
    return f"""
    <section style="margin-top:45px; border-top:2px solid #002d62; padding-top:25px;">
        <h3>Technical Update: {kws[0]}</h3>
        <p>Analyzing {kws[0]} under the 2026 OBBB (One, Big, Beautiful Bill) reveals significant shifts in filing requirements. 
        When evaluating {kws[1]} alongside {kws[2]}, it is clear that {kws[3]} triggers specific 1040-NR schedule adjustments. 
        Non-residents should note that {kws[4]} is now a primary focus of IRS audit algorithms.</p>
        <p>Ensure your refund velocity is maximized by utilizing the 
        <a href="{url}" style="font-weight:bold; color:#28a745;">IRS-Authorized E-File Portal</a> 
        configured for 2026 compliance.</p>
    </section>"""

# --- 3. THE EXECUTION ---

def run_expansion():
    if not GITHUB_TOKEN:
        print("❌ Error: CHAMELEON_TOKEN environment variable not set.")
        return

    g = Github(GITHUB_TOKEN)
    user = g.get_user()
    
    for site in SITES:
        print(f"🔄 Processing {site['repo']}...")
        kws = get_keywords(5)
        if not kws: break

        try:
            repo = user.get_repo(site['repo'])
            
            # 1. Update index.html
            file = repo.get_contents("index.html")
            html = file.decoded_content.decode()
            if "" in html:
                new_html = html.replace("", f"{build_content(kws, site['atid'])}\n")
                repo.update_file(file.path, f"Daily Authority: {kws[0]}", new_html, file.sha)
            
            # 2. Update sitemap.xml
            sm_xml = generate_sitemap(user.login, site['repo'])
            try:
                sm_file = repo.get_contents("sitemap.xml")
                repo.update_file(sm_file.path, "Sitemap Refresh", sm_xml, sm_file.sha)
            except:
                repo.create_file("sitemap.xml", "Initial Sitemap", sm_xml)
            
            print(f"✅ {site['repo']} Expanded.")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Failed {site['repo']}: {e}")

if __name__ == "__main__":
    run_expansion()
