import os
import json
import time
from github import Github

# --- 1. CONFIGURATION ---
GITHUB_TOKEN = os.getenv('CHAMELEON_TOKEN') 
KEYWORD_FILE = 'keywords.json'

# Your 10 niche repositories
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

# --- 2. SEO & CONTENT ENGINE ---

def get_keywords(count=5):
    """Pulls keywords and moves them to 'used' to prevent repetition."""
    if not os.path.exists(KEYWORD_FILE): return []
    with open(KEYWORD_FILE, 'r+') as f:
        data = json.load(f)
        batch = data['remaining'][:count]
        data['remaining'] = data['remaining'][count:]
        data['used'].extend(batch)
        f.seek(0); json.dump(data, f, indent=2); f.truncate()
    return batch

def generate_sitemap(user_login, repo_name):
    """Updates the Sitemap date to force a Google re-index."""
    today = time.strftime('%Y-%m-%d')
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>https://{user_login}.github.io/{repo_name}/</loc><lastmod>{today}</lastmod><priority>1.0</priority></url>
</urlset>"""

def build_content_block(kws, atid):
    """Generates an SEO-optimized authority section with affiliate tracking."""
    aff_url = f"https://www.linkconnector.com/ta.php?lc=007949054186005142&atid={atid}"
    today_long = time.strftime('%B %d, 2026')
    
    return f"""
    <section class="daily-update" style="margin-top:50px; border-top:3px solid #002d62; padding-top:25px; font-family: sans-serif;">
        <small style="color:#666;">AUTHORITY UPDATE: {today_long}</small>
        <h2 style="color:#002d62;">{kws[0]} & OBBB Impact</h2>
        <p>New 2026 guidelines suggest that <strong>{kws[0]}</strong> is now a major factor in refund velocity. 
        Taxpayers using <strong>{kws[1]}</strong> should evaluate their <strong>{kws[2]}</strong> 
        to ensure compliance with the latest OBBB bill standards.</p>
        
        <div style="background:#f4f7f6; border-left:5px solid #28a745; padding:20px; margin:20px 0;">
            <p><strong>Note:</strong> To bypass delays involving {kws[3]}, use the {kws[4]} protocol.</p>
            <a href="{aff_url}" style="display:inline-block; background:#28a745; color:white; padding:12px 25px; text-decoration:none; border-radius:5px; font-weight:bold;">File Now & Maximize Refund</a>
        </div>
    </section>
    """

# --- 3. THE MASTER RUNNER ---

def run_network():
    if not GITHUB_TOKEN:
        print("❌ Secret CHAMELEON_TOKEN is missing!")
        return

    g = Github(GITHUB_TOKEN)
    user = g.get_user()
    
    for site in SITES:
        print(f"🔄 Updating: {site['repo']}")
        kws = get_keywords(5)
        if not kws: break

        try:
            repo = user.get_repo(site['repo'])
            
            # 1. Update HTML
            file_data = repo.get_contents("index.html")
            content = file_data.decoded_content.decode()
            
            # Ensure Injection Point exists
            marker = ""
            if marker not in content:
                content = content.replace("</body>", f"{marker}\n</body>")
            
            # Update Content
            updated_content = content.replace(marker, f"{build_content_block(kws, site['atid'])}\n{marker}")
            repo.update_file(file_data.path, f"Update: {kws[0]}", updated_content, file_data.sha)
            
            # 2. Update Sitemap
            sitemap_content = generate_sitemap(user.login, site['repo'])
            try:
                sm_file = repo.get_contents("sitemap.xml")
                repo.update_file(sm_file.path, "Sitemap Refresh", sitemap_content, sm_file.sha)
            except:
                repo.create_file("sitemap.xml", "Initial Sitemap", sitemap_content)
                
            print(f"✅ {site['repo']} Done.")
            time.sleep(1) 
        except Exception as e: print(f"❌ Error in {site['repo']}: {e}")

if __name__ == "__main__":
    run_network()
