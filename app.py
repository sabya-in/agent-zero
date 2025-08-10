import os
from dotenv import load_dotenv
from core.analyzer import FinancialAnalyzer
from services.gemini_google import GeminiGoogleService
from services.query_optimizer import QueryOptimizer
from services.news_fetcher import GoogleNewsFetcher
from models.company import CompanyQuery
from utilities.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

def main():
    gemini = GeminiGoogleService()
    optimizer = QueryOptimizer(gemini)
    fetcher = GoogleNewsFetcher()

    user_stmt = input("Enter search (keywords, date, objective) in one line:\n").strip()
    logger.info("User statement: %s", user_stmt)

    optimized = optimizer.optimize(user_stmt)
    logger.info("Optimized query: %s", optimized.model_dump_json())

    # for step1 we stop here — show the optimized query
    print("\n=== OptimizedQuery (step1 output) ===")
    print(optimized.model_dump_json(indent=2))

    # (optionally) run the fetcher to see sample results — comment this out if you want step-1 only
    run_fetch = input("\nRun the news fetcher with this query? [y/N]: ").strip().lower()
    if run_fetch == "y":
        items = fetcher.search_with_optimized(optimized)
        logger.info("User statement: %s", items)
        print(f"\nFound {len(items)} items:")
        for i, it in enumerate(items, 1):
            print(f"{i}. {it['title']}\n   {it['link']}\n   {it['snippet']}\n")

if __name__ == "__main__":
    main()
