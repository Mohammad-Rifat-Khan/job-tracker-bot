import requests
import random
import time
import json
from bs4 import BeautifulSoup
from datetime import datetime
from filters import load_config, load_seen, save_seen, matches_filters

USER_AGENTS = [
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
]

def scrape_site(site, filters, seen):
    jobs = []
    page = 1
    while page <= filters.get("max_pages", 3):
        # Construct URL (handle pagination differently per site if needed)
        if "?" in site['base_url']:
            url = f"{site['base_url']}&page={page}"
        else:
            url = f"{site['base_url']}?page={page}"

        print(f"Scraping {site['name']} page {page}")
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            break
        soup = BeautifulSoup(r.text, 'lxml')
        job_blocks = soup.select(site['job_selector'])
        if not job_blocks:
            break
        for jb in job_blocks:
            text = jb.get_text(separator=" ", strip=True)
            if not matches_filters(text, filters):
                continue
            link = jb.find('a', href=True)
            job_id = hash((site['name'], link['href'] if link else text))
            if job_id in seen:
                continue
            seen.add(job_id)
            jobs.append({
                'job_id': job_id,
                'title': jb.find(['h2', 'h3']).get_text(strip=True) if jb.find(['h2','h3']) else 'N/A',
                'url': link['href'] if link else site['base_url'],
                'source': site['name'],
                'scraped_at': datetime.utcnow().isoformat()
            })
        page += 1
        time.sleep(random.uniform(2,5))
    return jobs

if __name__ == '__main__':
    config = load_config()
    seen = load_seen()
    all_new = []
    for site in config['sites']:
        new_jobs = scrape_site(site, config, seen)
        all_new.extend(new_jobs)
    save_seen(seen)
    print(json.dumps(all_new, indent=2))
