import os
import json
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
import dotenv
dotenv.load_dotenv()
#remove boilerplate/navigation sections

def clean_html_boilerplate(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Remove navigation and layout parts
    for tag in soup(["nav", "header", "footer", "aside", "form", "script", "style", "noscript"]):
        tag.extract()

    # Extract readable text
    text = soup.get_text(separator=" ")
    return " ".join(text.split())


#deduplicate text
def deduplicate_text(text: str) -> str:
    seen = set()
    unique_words = []

    for word in text.split():
        if word not in seen:
            seen.add(word)
            unique_words.append(word)

    return " ".join(unique_words)


#scrape URL
def scrape_url(url: str) -> dict:
    try:
        res = requests.get(url, timeout=12, max_redirects=3)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")

        title = soup.title.string.strip() if soup.title else ""

        meta_desc = soup.find("meta", attrs={"name": "description"})
        meta_keywords = soup.find("meta", attrs={"name": "keywords"})

        metadata = {
            "description": meta_desc["content"].strip() if meta_desc else None,
            "keywords": meta_keywords["content"].strip() if meta_keywords else None,
        }

        cleaned_text = clean_html_boilerplate(res.text)
        deduped_text = deduplicate_text(cleaned_text)

        return {
            "title": title,
            "text": deduped_text,
            "metadata": metadata
        }

    except Exception as e:
        return {"title": None, "text": None, "metadata": None, "error": str(e)}


#Tavily Search + Scraping Tool
def build_web_search_tool(max_results: int = 3):
    """ 
    Builds a web search tool using Tavily API and scraping.
    """
    @tool
    def web_search(query: str) -> str:
        """
        Performs Tavily web search and scrapes each resulting URL.
        Returns:
            {
                "action": "WebSearch",
                "action_input": [
                    {
                        "title": ...,
                        "url": ...,
                        "summary": Tavily summary,
                        "scraped_title": ...,
                        "scraped_text": ...,
                        "metadata": {...}
                    },
                    ...
                ]
            }
        """
        print("Invoking Web Search Tool......................")
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return json.dumps({
                "error": "TAVILY_API_KEY is not set in environment"
            })

        tavily_payload = {
            "api_key": api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
        }

        try:
            r = requests.post("https://api.tavily.com/search", json=tavily_payload, timeout=12)
            r.raise_for_status()
            tavily_data = r.json()
        except Exception as e:
            return json.dumps({"error": f"Tavily API error: {e}"})

        results = []
        for item in tavily_data.get("results", []):
            url = item.get("url")

            scraped = scrape_url(url)

            results.append({
                "title": item.get("title"),
                "summary": item.get("content"),
                "scraped_title": scraped.get("title"),
                "scraped_text": scraped.get("text"),
            })

        return json.dumps({
            "action": "WebSearch",
            "action_input": results
        })
    
    web_search.name = "WebSearch"
    web_search.description = "Use this tool when the user needs external information. It performs a Tavily web search, scrapes all returned URLs, cleans boilerplate, deduplicates text, and returns high-quality context. After using this tool , alwayas use the context relevance tool to ensure the context is relevant to the user question."

    return web_search

