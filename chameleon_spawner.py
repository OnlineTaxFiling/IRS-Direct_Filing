import os
import json
import time
from github import Github

# --- 1. CONFIGURATION ---
GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN_HERE'  # Classic PAT with 'repo' scope
AFFILIATE_BASE = "https://www.linkconnector.com/ta.php?lc=007949054186005142"

# Today's 10 Target Niches
TODAY_BATCH = [
    {"repo": "IRS-Direct-Filing-2026", "title": "Official IRS Direct Filing Portal", "atid": "IRS_Direct"},
    {"repo": "Visa-Tax-Authority", "title": "2026 Visa Holder Tax Resource", "atid": "Visa_Tax"},
    {"repo": "F1-J1-Student-Refunds", "title": "Student & Scholar Tax Recovery", "atid": "Student_Tax"},
    {"repo": "OBBB-Tax-Bill-Breakdown", "title": "2026 OBBB Tax Bill Encyclopedia", "atid": "OBBB_Law"},
    {"repo": "Expat-Tax-Direct-2026", "title": "Expatriate Federal Filing Hub", "atid": "Expat_Hub"},
    {"repo": "Overtime-Tip-Deductions", "title": "No Tax on Tips & Overtime Guide", "atid": "Tips_OT"},
    {"repo": "Senior-Tax-Bonus-Portal", "title": "Senior $6,000 Bonus Filing Tool", "atid": "Senior_Bonus"},
    {"repo": "Car-Loan-Interest-Refunds", "title": "Vehicle Interest Deduction Portal", "atid": "Car_Loan"},
    {"repo": "Non-Resident-Audit-Secure", "title": "Audit-Secure Non-Resident Portal", "atid": "Audit_Safe"},
    {"repo": "Digital-Nomad-US-Taxes", "title": "2026 Nomad Tax Compliance Hub", "atid": "Nomad_Tax"}
]

# --- 2. THE SEED HTML GENERATOR ---
def generate_seed_html(title, atid):
    tracking_link = f"{AFFILIATE_BASE}&atid={atid}"
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><title>{title} | 2026 Authority</title>
    <style>
        :root {{ --primary: #002d62; --accent: #28a745; --light: #f4f7f9; --alert: #d9534f; }}
        body {{ font-family: "Segoe UI", sans-serif; line-height: 1.8; color: #333; margin: 0; display: flex; background: var(--light); }}
        nav {{ width: 300px; height: 100vh; position: sticky; top: 0; background: white; border-right: 1px solid #ddd; padding: 25px; overflow-y: auto; }}
        .timer-box {{ background: #eee; padding: 15px; border-radius: 5px; margin-bottom: 20px; font-size: 0.85rem; border-left: 4px solid var(--alert); }}
        main {{ flex: 1; padding: 50px; max-width: 1000px; background: white; min-height: 200vh; }}
        .cta-banner {{ background: var(--primary); color: white; padding: 30px; border-radius: 8px; text-align: center; margin: 40px 0; }}
        .cta-banner a {{ display: inline-block; background: var(--accent); color: white; padding: 15px 35px; border-radius: 5px; text-decoration: none; font-weight: bold; }}
        footer {{ position: fixed; bottom: 0; left: 0; width: 100%; background: #222; color: white; text-align: center; padding: 15px; }}
        footer a {{ color: #51cf66; font-weight: bold; }}
    </style>
</head>
<body>
<nav>
    <div class="timer-box"><strong>⏳ Tax Day Countdown</strong><span id="t1"></span></div>
    <div class="timer-box" style="border-left-color: var(--primary);"><strong>📅 Extension Deadline</strong><span id="t2"></span></div>
    <h2>{title} Links</h2><hr>
    <a href="#intro">2026 Overview</a><a href="#obbb">OBBB Tax Codes</a>
</nav>
<main>
    <h1>{title}</h1>
    <p>Welcome to the 2026 {title}. This is a living document updated daily to reflect the 'One, Big, Beautiful Bill' (OBBB) changes including the $16,100 standard deduction.</p>
    <div class="cta-banner">
        <h2>File Your 2026 Taxes Now</h2>
        <a href="{tracking_link}">Start IRS-Authorized E-File</a>
    </div>
    <section id="obbb">
        <h2>The 2026 OBBB Advantage</h2>
        <p>The OBBB has transformed filing for {title}. Claim your no-tax-on-tips and the $10,000 vehicle interest deduction today.</p>
    </section>
    </main>
<footer>Need your refund faster? <a href="{tracking_link}">Click here to E-File now.</a></footer>
<script>
    function u(){{
        const n=new Date().getTime();
        const d1=new Date("April 15, 2026").getTime();
        const d2=new Date("June 15, 2026").getTime();
        document.getElementById("t1").innerHTML=Math.floor((d1-n)/(86400000))+"d remaining";
        document.getElementById("t2").innerHTML=Math.floor((d2-n)/(86400000))+"d remaining";
    }} setInterval(u,60000);u();
</script>
</body></html>
"""

# --- 3. THE MANEUVER EXECUTION ---
def execute_maneuver():
    g = Github(GITHUB_TOKEN)
    user = g.get_user()

    for site in TODAY_BATCH:
        try:
            print(f"🛠️ Creating Repository: {site['repo']}...")
            repo = user.create_repo(site['repo'], description=site['title'], auto_init=True)
            
            # Generate the unique HTML
            html_content = generate_seed_html(site['title'], site['atid'])
            
            # Push the file
            repo.create_file("index.html", "Chameleon Spawn: 2026 Initial Seed", html_content, branch="main")
            print(f"✅ Success! URL: https://{user.login}.github.io/{site['repo']}/")
            
            time.sleep(5) # Delay to satisfy API limits
        except Exception as e:
            print(f"❌ Failed {site['repo']}: {e}")

if __name__ == "__main__":
    execute_maneuver()
