# models/search.py
import os
from pydantic import BaseModel
from typing import Optional, List

class UserSearchInput(BaseModel):
    """
    Single-line user instruction which includes keywords, date and objective.
    Example: "Find news about Tesla between 2019-01-01 and 2019-12-31 focusing on product recalls and investor sentiment"
    """
    statement: str

class OptimizedQuery(BaseModel):
    # Final statement to pass to the search API (can include operators)
    statement: str

    # Optional site restrictions (e.g. ["reuters.com", "bloomberg.com"])
    site_restrictions: Optional[List[str]] = []

    # Absolute dates in ISO format (YYYY-MM-DD). If not present, set to None.
    date_from: Optional[str] = None
    date_to: Optional[str] = None

    # Prefered number of results
    num_results: int = int(os.getenv("SEARCH_RESULTS_LIMIT", 6))

    # Language & sorting hints
    language: Optional[str] = "en"
    #sort: Optional[str] = "relevance"  # e.g., "date" or "relevance"

    # Any additional operators or extra filters (string appended to query)
    extra_filters: Optional[str] = None
