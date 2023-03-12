import argparse
import requests
from bs4 import BeautifulSoup
import json
from typing import List

def get_image_urls(url: str) -> List[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    urls = []
    for img in img_tags:
        if 'src' in img.attrs:
            urls.append(img['src'])
    return urls

def get_links(url: str) -> List[str]:
    links = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.find_all("a"):
        href = link.get("href")
        if href is not None and (href.startswith("http://") or href.startswith("https://")):
            links.append(href)
    return links

def crawl(url: str, depth: int, results: List[dict], visited: set, current_depth: int = 0):
    if depth == 0 or url in visited or url is None:
        return
    visited.add(url)
    image_urls = get_image_urls(url)
    for img_url in image_urls:
        results.append({
            "imageUrl": img_url,
            "sourceUrl": url,
            "depth": current_depth
        })
    links = get_links(url)
    for link in links:
        crawl(link, depth-1, results, visited, current_depth+1)

def save_results(results: List[dict]):
    data = {
        "results": results
    }
    with open('results.json', 'w') as outfile:
        json.dump(data, outfile)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Web Crawler')
    parser.add_argument('start_url', type=str, help='Starting URL for crawling')
    parser.add_argument('depth', type=int, help='Depth of crawling')
    args = parser.parse_args()
    start_url = args.start_url
    depth = args.depth
    results = []
    visited = set()
    crawl(start_url, depth, results, visited)
    save_results(results)
