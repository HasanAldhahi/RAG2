import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_nav_links(url, base_url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    nav_div = soup.find('div', id='dokuwiki__aside', class_='_gwdg-nav')
    
    if not nav_div:
        print("Navigation bar not found.")
        return []

    links = []

    for a_tag in nav_div.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(base_url, href)
        links.append(full_url)
    
    return links

def get_li_links(url, base_url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    nav_div = soup.find('div', id='dokuwiki__aside', class_='_gwdg-nav')
    
    if not nav_div:
        print("Navigation bar not found.")
        return []

    li_links = []

    for li in nav_div.find_all('li'):
        a_tag = li.find('a', href=True)
        if a_tag:
            href = a_tag['href']
            full_url = urljoin(base_url, href)
            li_links.append(full_url)
    
    return li_links

def save_links_to_file(links, filename):
    with open(filename, 'w') as file:
        for link in links:
            file.write(f"{link}\n")

base_url = 'https://docs.gwdg.de'
start_url = 'https://docs.gwdg.de/doku.php?id=de:start'

# Step 1: Get initial navigation links
nav_links = get_nav_links(start_url, base_url)

# Step 2: Iterate through each link and get links from li components
all_li_links = set()  # Use a set to store unique links
for link in nav_links:
    li_links = get_li_links(link, base_url)
    all_li_links.update(li_links)  # Add new links to the set

# Step 3: Save all the collected links to a text file
if all_li_links:
    save_links_to_file(all_li_links, 'li_links.txt')
    print(f"Saved {len(all_li_links)} unique links to li_links.txt")
else:
    print("No links found.")
