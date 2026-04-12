import os
import json
import time
from github import Github

# --- 1. CONFIGURATION ---
# Fetches from GitHub Secrets for security
GITHUB_TOKEN = os.getenv('CHAMELEON_TOKEN') 
KEYWORD_FILE = 'keywords.json'

# List of your 10 active 2026 Tax niches
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

# --- 2. THE LOGIC ENGINES ---

def get_keywords(count=5):
    """Pulls keywords and moves them to 'used' to prevent repetition."""
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
    """Refreshes the Sitemap date to force a re-index."""
    today = time.strftime('%Y-%m-%d')
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>https://{user_login}.github.io/{repo_name}/</loc><lastmod>{today}</lastmod><priority>1.0</priority></url>
</urlset>"""

def build_enhanced_block(kws, atid):
    """Generates an SEO-optimized authority section with affiliate tracking."""
    aff_url = f"https://www.linkconnector.com/ta.php?lc=007949054186005142&atid={atid}"
    today_long = time.strftime('%B %d, %2026')
    
    return f"""
    <section class="daily-update" style="margin-top:50px; border-top:3px solid #002d62; padding-top:25px;">
        <small style="color:#666; text-transform:uppercase;">Verified Update: {today_long}</small>
        <h2 style="color:#002d62;">{kws[0]} & OBBB Compliance</h2>
        <p>In the latest 2026 tax cycle, <strong>{kws[0]}</strong> has emerged as a high-priority item for IRS scrutiny. 
        Effective immediately, taxpayers utilizing <strong>{kws[1]}</strong> must cross-verify their <strong>{kws[2]}</strong> 
        data to ensure the OBBB standard deduction is applied correctly.</p>
        
        <div style="background:#f8f9fa; border-left:5px solid #28a745; padding:20px; margin:20px 0;">
            <p><strong>Urgent Notice:</strong> To avoid processing delays associated with {kws[3]}, it is recommended 
            to utilize the {kws[4]} protocol via an authorized portal.</p>
            <a href="{aff_url}" style="display:inline-block; background:#28a745; color:white; padding:12px 25px; text-decoration:none; border-radius:5px; font-weight:bold;">Secure Your 2026 Refund Now</a>
        </div>
    </section>
    """

# --- 3. THE MASTER RUNNER ---

def run_network_expansion():
    if not GITHUB_TOKEN:
        print("❌ CRITICAL ERROR: CHAMELEON_TOKEN environment variable is missing.")
        return

    g = Github(GITHUB_TOKEN)
    user = g.get_user()
    
    for site in SITES:
        print(f"🚀 Processing: {site['repo']}")
        kws = get_keywords(5)
        if not kws:
            print(f"⚠️ Out of keywords for {site['repo']}. Please refill keywords.json.")
            break

        try:
            repo = user.get_repo(site['repo'])
            
            # 1. Update index.html
            file_data = repo.get_contents("index.html")
            content = file_data.decoded_content.decode()
            
            # Fix: Ensure Injection Point exists
            marker = ""
            if marker not in content:
                content = content.replace("</body>", f"{marker}\n</body>")
            
            # Enhancement: Update Meta Description for SEO
            new_meta = f'<meta name="description" content="Latest 2026 update on {kws[0]} and {kws[1]} filing requirements.">'
            if '<meta name="description"' in content:
                # Basic string replacement for simplicity
                import re
                content = re.sub(r'<meta name="description" content=".*?">', new_meta, content)
            
            # Inject new content
            new_block = build_enhanced_block(kws, site['atid'])
            updated_content = content.replace(marker, f"{new_block}\n{marker}")
            
            repo.update_file(file_data.path, f"OBBB Update: {kws[0]}", updated_content, file_data.sha)
            
            # 2. Refresh Sitemap
            sitemap_content = generate_sitemap(user.login, site['repo'])
            try:
                sm_file = repo.get_contents("sitemap.xml")
                repo.update_file(sm_file.path, "Daily Sitemap Ping", sitemap_content, sm_file.sha)
            except:
                repo.create_file("sitemap.xml", "Initial Sitemap", sitemap_content)
                
            print(f"✅ SUCCESS: {site['repo']} updated and indexed.")
            time.sleep(2) # Prevent GitHub API rate-limiting

        except Exception as e:
            print(f"❌ ERROR in {site['repo']}: {str(e)}")

if __name__ == "__main__":
    run_network_expansion()
