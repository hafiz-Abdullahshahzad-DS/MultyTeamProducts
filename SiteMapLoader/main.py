import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone


# Function to fetch and filter sitemap URLs by lastmod date
def fetch_updated_links(sitemap_url, lastmod_cutoff):
    response = requests.get(sitemap_url)
    
    if response.status_code == 200:
        # Parse XML content
        root = ET.fromstring(response.content)
        
        # Iterate through each URL in the sitemap
        updated_links = []
        for url in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
            lastmod = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod')
            
            if lastmod is not None:
                # Parse lastmod date using fromisoformat
                lastmod_date = datetime.fromisoformat(lastmod.text)
                if lastmod_date >= lastmod_cutoff:
                    updated_links.append(loc)
        
        return updated_links
    else:
        print(f"Failed to retrieve sitemap. Status code: {response.status_code}")
        return []

# URL of the website sitemap
sitemap_url = 'https://thecurrent.pk/post-sitemap.xml'


past_days = 1
# Define the cutoff date (e.g., get links updated in the last 7 days)
cutoff_date = datetime.now(timezone.utc) - timedelta(days=past_days)  # Ensure cutoff is in UTC

# Fetch updated links
updated_links = fetch_updated_links(sitemap_url, cutoff_date)
print(f"Total No of links update in {past_days} day are {len(updated_links)}")

