# services/query_optimizer.py
import os
import json
from typing import Optional
from models.news import OptimizedQuery
from utilities.logger import get_logger
from services.gemini_google import GeminiGoogleService  # your existing service
logger = get_logger(__name__)

class QueryOptimizer:
    def __init__(self, gemini_service: GeminiGoogleService):
        self.gemini = gemini_service

    def optimize(self, user_statement: str) -> OptimizedQuery:
        """
        Send the user's single statement to Gemini and ask for a strict JSON response
        with fields matching OptimizedQuery.
        """
        prompt = f"""
                    You are a Google search query optimizer for news retrieval. 
                    Input: a single-line user instruction describing keywords, dates, and the objective of the search.

                    Produce JSON ONLY (no commentary) with this schema:
                    {{
                    "query": "optimized search query string for Google (use quotes, site:, -exclude, OR as needed)",
                    "site_restrictions": ["reuters.com","nytimes.com"],   # or [] if none
                    "date_from": "YYYY-MM-DD" or null,
                    "date_to": "YYYY-MM-DD" or null,
                    "num_results": 5,
                    "language": "en",
                    "extra_filters": "-site:example.com"              # optional
                    }}

                    Rules:
                    - Keep "query" concise and focused (single string). Use Google operators (site:, quotes, -term) where useful.
                    - If the user gave absolute dates, set date_from/date_to. If they gave relative ranges (like 'past week') either set date_from/date_to or put a note in extra_filters.
                    - If a field is not applicable, return null or empty list as appropriate.

                    User instruction:
                    \"\"\"{user_statement}\"\"\"
                    """

        # call Gemini -- returns a string (expected to be JSON)
        raw = None
        try:
            raw = self.gemini.get_analysis(prompt, "google_search")
            print(raw)
            logger.debug("Gemini raw optimizer output: %s", raw)
            # try strict parse
            parsed = json.loads(raw)
            return OptimizedQuery(**parsed)
        except Exception as e:
            logger.exception("Failed to parse Gemini optimizer response: %s", e)
            # Fallback: create a basic OptimizedQuery by using the raw statement as the query
            num_results = int(os.getenv("SEARCH_RESULTS_LIMIT", 6))
            fallback = OptimizedQuery(query=user_statement, num_results=num_results)
            # attempt heuristics: try to extract YYYY-MM-DD date tokens if present
            try:
                import re
                dates = re.findall(r"\b\d{4}-\d{2}-\d{2}\b", user_statement)
                if len(dates) >= 1:
                    fallback.date_from = dates[0]
                if len(dates) >= 2:
                    fallback.date_to = dates[1]
            except Exception:
                pass
            logger.info("Returning fallback optimized query: %s", fallback.model_dump_json())
            return fallback
