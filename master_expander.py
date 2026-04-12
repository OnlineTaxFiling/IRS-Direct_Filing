import os
import json
import time
from github import Github

# --- 1. CONFIGURATION ---
# Replace with your Classic PAT (must have 'repo' scope)
GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN_HERE' 
KEYWORD_FILE = 'keywords.json'

# This list must match the 'repo' and 'atid' values from your Spawner
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

# --- 2. THE UTILITY FUNCTIONS ---

def get_daily_keywords(count=5):
    """Pulls unique keywords and moves them to the 'used' list."""
    if not os.path.exists(KEYWORD_FILE):
        return []
    with open(KEYWORD_FILE, 'r+') as f:
        data = json.load(f)
        selected = data['remaining'][:count]
        data['remaining'] = data['remaining'][count:]
        data['used'].extend(selected)
        f.seek(0); json.dump(data, f, indent=2); f.truncate()
    return selected

def build_injection_block(keywords, atid):
    """Creates a 2026-compliant content block with affiliate tracking."""
    affiliate_url = f"https://www.linkconnector.com/ta.php?lc=007949054186005142&atid={atid}"
    return f"""
    <section style="margin-top: 45px; border-top: 1px solid #ddd; padding-top: 25px;">
        <h3>2026 Regulatory Review: {keywords[0]}</h3>
        <p>In the current fiscal landscape, {keywords[0]} is a critical component for those filing under the OBBB guidelines. 
        Recent updates suggest that {keywords[1]} and {keywords[2]} must be filed using the enhanced 1040-NR schedules to ensure 
        maximum refund velocity. Experts note that {keywords[3]} is often overlooked, leading to processing delays.</p>
        
        <div style="background: #eef9f1; padding: 20px; border-radius: 6px; border-left: 5px solid #28a745;">
            <strong>Pro Tip:</strong> Most {keywords[4]} errors can be avoided by using the 
            <a href="{affiliate_url}" style="color: #002d62; font-weight: bold;">Official 2026 E-File Interface</a>, 
            which automatically updates for all 'One, Big, Beautiful Bill' provisions.
        </div>
    </section>
    """

def update_sitemap(repo, user_login, repo_name):
    """Updates the sitemap.xml to trigger a re-index ping."""
    sitemap_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://{user_login}.github.io/{repo_name}/</loc>
        <lastmod>{time.strftime('%Y-%m-%d')}</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
</urlset>"""
    try:
        f = repo.get_contents("sitemap.xml")
        repo.update_file(f.path, "Daily Sitemap Refresh", sitemap_xml, f.sha)
    except:
        repo.create_file("sitemap.xml", "Initial Sitemap", sitemap_xml)

# --- 3. THE MAIN LOOP ---

def run_expansion():
    g = Github(GITHUB_TOKEN)
    user = g.get_user()
    
    for site in SITES:
        print(f"🔄 Processing {site['repo']}...")
        keywords = get_daily_keywords(5)
        
        if not keywords:
            print(f"⚠️ Out of keywords for {site['repo']}")
            continue

        try:
            repo = user.get_repo(site['repo'])
            # 1. Update index.html
            file_content = repo.get_contents("index.html")
            html = file_content.decoded_content.decode()
            
            marker = ''
            if marker in html:
                new_block = build_injection_block(keywords, site['atid'])
                updated_html = html.replace(marker, f"{new_block}\n{marker}")
                
                repo.update_file(
                    file_content.path, 
                    f"Authority Injection: {keywords[0]}", 
                    updated_html, 
                    file_content.sha
                )
                
                # 2. Refresh Sitemap
                update_sitemap(repo, user.login, site['repo'])
                print(f"✅ {site['repo']} successfully updated.")
            else:
                print(f"❌ Marker missing in {site['repo']}")

        except Exception as e:
            print(f"❌ Error in {site['repo']}: {e}")
        
        time.sleep(2) # Prevent API abuse triggers

if __name__ == "__main__":
    run_expansion()
