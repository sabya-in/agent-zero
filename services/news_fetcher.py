# services/news_fetcher.py  (add method or update existing class)
import os
import requests
from dotenv import load_dotenv
from models.news import OptimizedQuery
from utilities.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

class GoogleNewsFetcher:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.cx = os.getenv("GOOGLE_CX")
        if not self.api_key or not self.cx:
            raise ValueError("GOOGLE_API_KEY and GOOGLE_CX must be set in .env")

    def _build_query_from_optimized(self, opt: OptimizedQuery) -> (str, dict):
        q = opt.statement.strip()
        # apply site restrictions into the query string
        if opt.site_restrictions:
            q += " " + " ".join(f"site:{s}" for s in opt.site_restrictions)
        # apply extra_filters
        if opt.extra_filters:
            q += " " + opt.extra_filters

        # Params we'll pass to API
        params = {"key": self.api_key, "cx": self.cx, "q": q, "num": opt.num_results}

        # If the user provided absolute date range, add after:/before: operators to query.
        # (These operators work in Google Search; Custom Search API sometimes prefers dateRestrict for relative ranges.)
        if opt.date_from:
            q += f" after:{opt.date_from}"
            params["q"] = q  # update q in params
        if opt.date_to:
            q += f" before:{opt.date_to}"
            params["q"] = q

        # If user gave relative range like 'past 7 days', use dateRestrict if possible (d[number])
        # dateRestrict supports formats like d7, m1, y1 (past days/months/years) per Custom Search docs.
        # We'll try to guess a relative range from extra_filters (optional).
        # You can directly set params["dateRestrict"]="d7" if you receive that preference from Gemini.
        return q, params

    def search_with_optimized(self, opt: OptimizedQuery):
        q, params = self._build_query_from_optimized(opt)
        logger.info("Running search q=%s params=%s", q, {k: v for k, v in params.items() if k != "key"})
        logger.info("Response",params)
        resp = requests.get("https://www.googleapis.com/customsearch/v1", params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        logger.info("response", data)
        items = []
        for item in data.get("items", []):
            items.append({
                "title": item.get("title"),
                "snippet": item.get("snippet"),
                "link": item.get("link"),
                # published date might not be directly available in CSE result; you may need to fetch the page
            })
        return items
