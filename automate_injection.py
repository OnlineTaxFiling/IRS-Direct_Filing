import os
import json
import time
from github import Github

# --- 1. CONFIGURATION ---
# Replace with your actual Classic PAT (Personal Access Token)
GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN_HERE' 
KEYWORD_FILE = 'keywords.json'

# This list manages your "Tree Network"
# For each site, you can set a unique tracking ID (atid)
SITES = [
    {"repo": "IRS-Direct_Filing", "atid": "IRS_Direct_Pillar"},
    {"repo": "Visa-Tax-Guide-2026", "atid": "Visa_Authority_Pillar"},
    {"repo": "Student-Tax-Exemptions", "atid": "F1_J1_Exempt_Pillar"},
    {"repo": "OBBB-Tax-Bill-Updates", "atid": "OBBB_Official_Pillar"},
    {"repo": "Expat-Refund-Central", "atid": "Expat_Refund_Pillar"},
    {"repo": "Overtime-Tax-Deductions", "atid": "Tips_Overtime_Pillar"},
    {"repo": "Senior-Tax-Bonuses", "atid": "Senior_6000_Pillar"},
    {"repo": "Car-Loan-Interest-Refund", "atid": "Vehicle_Loan_Pillar"},
    {"repo": "Non-Resident-Checklist", "atid": "Checklist_Pillar"},
    {"repo": "Digital-Nomad-US-Taxes", "atid": "Nomad_Tax_Pillar"}
]

# --- 2. CORE LOGIC ---

def get_daily_keywords(count=10):
    """Pulls keywords and moves them to 'used' so sites remain unique."""
    if not os.path.exists(KEYWORD_FILE):
        print(f"❌ Error: {KEYWORD_FILE} not found.")
        return []

    with open(KEYWORD_FILE, 'r+') as f:
        data = json.load(f)
        selected = data['remaining'][:count]
        data['remaining'] = data['remaining'][count:]
        data['used'].extend(selected)
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
    return selected

def build_content_block(keywords, atid):
    """Generates the HTML <div> for injection with your affiliate ID intact."""
    affiliate_url = f"https://www.linkconnector.com/ta.php?lc=007949054186005142&atid={atid}"
    
    # This block follows your 'Long-Form Architect' requirements (3-line paragraphs)
    return f"""
    <section style="margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px;">
        <h3>Technical Focus: {keywords[0]} and {keywords[1]}</h3>
        <p>Current 2026 data indicates that {keywords[0]} is a pivotal factor in maximizing non-resident returns under the OBBB. 
        Taxpayers utilizing these specific provisions have seen a marked increase in refund velocity. 
        Ensuring your documentation for {keywords[1]} is precise prevents common filing delays.</p>
        
        <div style="background: #f8f9fa; padding: 15px; border-left: 4px solid #28a745;">
            <strong>Pro Tip:</strong> To automate these calculations, use the 
            <a href="{affiliate_url}">IRS-Authorized E-File Portal</a> 
            which includes the latest 2026 OBBB patch.
        </div>
    </section>
    """

def update_all_sites():
    """Iterates through your SITES list and performs the injection."""
    g = Github(GITHUB_TOKEN)
    user = g.get_user()
    
    for site in SITES:
        print(f"🔄 Processing {site['repo']}...")
        keywords = get_daily_keywords(5) # Get 5 unique keywords per update
        
        if not keywords:
            print(f"⚠️ No more keywords left for {site['repo']}")
            continue

        try:
            repo = user.get_repo(site['repo'])
            contents = repo.get_contents("index.html")
            current_html = contents.decoded_content.decode()

            # The Secret Logic: Injecting at the marker
            marker = ''
            if marker in current_html:
                new_block = build_content_block(keywords, site['atid'])
                updated_html = current_html.replace(marker, f"{new_block}\n{marker}")

                repo.update_file(
                    contents.path, 
                    "Daily Freshness Injection: April 2026 Authority", 
                    updated_html, 
                    contents.sha
                )
                print(f"✅ {site['repo']} updated successfully.")
            else:
                print(f"❌ Marker not found in {site['repo']}.")

        except Exception as e:
            print(f"❌ Failed to update {site['repo']}: {e}")
        
        # Sleep to avoid GitHub API rate limiting
        time.sleep(2)

if __name__ == "__main__":
    update_all_sites()
