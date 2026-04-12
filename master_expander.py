import os
import json
import time
from github import Github

# --- SETTINGS ---
GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN_HERE'
KEYWORD_FILE = 'keywords.json'

# This matches the 'atid' and 'repo' names from your Spawner
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

def get_keywords(count=5):
    with open(KEYWORD_FILE, 'r+') as f:
        data = json.load(f)
        batch = data['remaining'][:count]
        data['remaining'] = data['remaining'][count:]
        data['used'].extend(batch)
        f.seek(0); json.dump(data, f, indent=2); f.truncate()
    return batch

def expand_all():
    g = Github(GITHUB_TOKEN)
    user = g.get_user()

    for site in SITES:
        print(f"📈 Expanding {site['repo']}...")
        keywords = get_keywords(5)
        if not keywords: break

        # Generate the 500-word Authority Injection
        new_content = f"""
        <section style="margin-top:50px; border-top:2px solid #002d62; padding-top:20px;">
            <h3>2026 Deep Dive: {keywords[0]} & {keywords[1]}</h3>
            <p>Under the 2026 OBBB framework, {keywords[0]} has become a focal point for non-resident optimization. 
            By cross-referencing {keywords[1]} with current IRS Direct Filing pilots, taxpayers can often 
            identify additional credits related to {keywords[2]}.</p>
            <p>To ensure 100% compliance with these specific 2026 codes, utilizing an 
            <a href="https://www.linkconnector.com/ta.php?lc=007949054186005142&atid={site['atid']}">IRS-Authorized portal</a> 
            is recommended to avoid the 'Manual Review' queue.</p>
        </section>
        """

        try:
            repo = user.get_repo(site['repo'])
            file = repo.get_contents("index.html")
            html = file.decoded_content.decode()

            if "" in html:
                updated = html.replace("", f"{new_content}\n")
                repo.update_file(file.path, f"Daily Authority Expansion: {keywords[0]}", updated, file.sha)
                print(f"✅ {site['repo']} Updated.")
            
            time.sleep(2) # Avoid API rate limits
        except Exception as e:
            print(f"❌ Error on {site['repo']}: {e}")

if __name__ == "__main__":
    expand_all()
