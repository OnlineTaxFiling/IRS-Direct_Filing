import os
import json
import time

# --- 1. CONFIGURATION ---
KEYWORD_FILE = 'keywords.json'
# We are now using FOLDERS instead of separate REPOS
NICHES = [
    "IRS-Direct-Filing", "Visa-Tax", "Student-Refunds", 
    "OBBB-Law", "Expat-Tax", "Tips-OT", "Senior-Bonus"
]

def get_keywords(count=5):
    if not os.path.exists(KEYWORD_FILE): return []
    with open(KEYWORD_FILE, 'r+') as f:
        data = json.load(f)
        batch = data['remaining'][:count]
        data['remaining'] = data['remaining'][count:]
        data['used'].extend(batch)
        f.seek(0); json.dump(data, f, indent=2); f.truncate()
    return batch

def build_page(kw, niche):
    return f"""
    <html>
    <head><title>{kw} - 2026 Tax Update</title></head>
    <body style="font-family:sans-serif; padding:40px;">
        <h1>{kw}</h1>
        <p>Latest updates regarding the OBBB 2026 tax cycle and {niche}.</p>
        <a href="https://www.linkconnector.com/ta.php?lc=007949054186005142&atid={niche}" 
           style="background:green; color:white; padding:10px; border-radius:5px;">Check Refund Status</a>
    </body>
    </html>
    """

def run_internal_expansion():
    for niche in NICHES:
        if not os.path.exists(niche):
            os.makedirs(niche)
        
        kws = get_keywords(3)
        for kw in kws:
            # Create a unique filename for every keyword
            filename = kw.lower().replace(" ", "-") + ".html"
            path = os.path.join(niche, filename)
            
            with open(path, "w") as f:
                f.write(build_page(kw, niche))
            print(f"✅ Created {path}")

if __name__ == "__main__":
    run_internal_expansion()
