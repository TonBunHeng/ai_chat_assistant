import re
import requests
from typing import List, Dict, Any

class WebSearchService:
    """
    Live Google / Web Search Service for Cambodia Tourism.
    Fetches real-time search snippets from the web when local database lacks exact coverage.
    """
    def search_google_web(self, query: str, max_results: int = 4) -> List[Dict[str, Any]]:
        """Perform a live web search for the given query."""
        if not query or not query.strip():
            return []

        search_query = f"{query.strip()} Cambodia tourism travel"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        results = []

        # 1. Try DuckDuckGo Instant Search / HTML API
        try:
            url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(search_query)}"
            res = requests.get(url, headers=headers, timeout=4)
            if res.status_code == 200:
                html = res.text
                
                # Regex match for result snippets
                snippets = re.findall(r'<a class="result__snippet[^">]*>(.*?)</a>', html, re.DOTALL)
                titles = re.findall(r'<a class="result__a"[^">]*>(.*?)</a>', html, re.DOTALL)
                urls = re.findall(r'<a class="result__url"[^">]*>(.*?)</a>', html, re.DOTALL)

                for i in range(min(len(titles), len(snippets))):
                    clean_title = re.sub(r'<[^>]+>', '', titles[i]).strip()
                    clean_snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip()
                    clean_url = urls[i].strip() if i < len(urls) else ""

                    if clean_title and clean_snippet:
                        results.append({
                            "name": clean_title,
                            "title": clean_title,
                            "description": clean_snippet,
                            "snippet": clean_snippet,
                            "location": "Live Google / Web Search",
                            "source_type": "google_web",
                            "category": "Google Search",
                            "url": f"https://{clean_url}" if clean_url and not clean_url.startswith("http") else clean_url
                        })

                    if len(results) >= max_results:
                        break
        except Exception as e:
            print(f"[WebSearchService] Search error: {e}")

        # 2. Fallback Wikipedia API if DuckDuckGo returned no snippets
        if not results:
            try:
                wiki_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(query)}&format=json"
                res = requests.get(wiki_url, headers=headers, timeout=4)
                if res.status_code == 200:
                    data = res.json()
                    search_list = data.get("query", {}).get("search", [])
                    for item in search_list[:max_results]:
                        clean_snippet = re.sub(r'<[^>]+>', '', item.get("snippet", "")).strip()
                        results.append({
                            "name": item.get("title", ""),
                            "title": item.get("title", ""),
                            "description": clean_snippet,
                            "snippet": clean_snippet,
                            "location": "Wikipedia Google Search Index",
                            "source_type": "google_web",
                            "category": "Google Search"
                        })
            except Exception as e:
                print(f"[WebSearchService] Wiki fallback error: {e}")

        return results

web_search_service = WebSearchService()
