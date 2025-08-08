# import os
# from google import genai

# # The client gets the API key from the environment variable `GEMINI_API_KEY`.
# api_key = os.getenv("GEMINI_API_KEY")
# if not api_key:
#     raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

# client = genai.Client(api_key=api_key)

# prompt = input("Ask Gemini something: ")

# response = client.models.generate_content(
#     model="gemini-2.5-flash", contents=prompt
# )
# print(response.text)

import os
from dotenv import load_dotenv
from core.analyzer import FinancialAnalyzer
from services.gemini_google import GeminiGoogleService
from models.company import CompanyQuery
from utilities.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

def main():
    try:
        logger.info("Starting Financial Analyzer App...")

        # Take inputs from user
        company_name = input("Enter the company name: ").strip()
        ticker = input("Enter the ticker symbol: ").strip()
        year = int(input("Enter the financial year (YYYY): ").strip())
        description = input("Enter a short company description: ").strip()

        logger.info(f"User provided company: {company_name}, ticker: {ticker}, year: {year}")

        # Build query
        query = CompanyQuery(
            name=company_name,
            ticker=ticker,
            year=year
        )

        # Create Gemini service
        gemini_service = GeminiGoogleService()

        # Initialize analyzer
        analyzer = FinancialAnalyzer(gemini_service)

        # Run analysis
        insights = analyzer.analyze(query)

        if insights:
            print("\n=== Financial Insights ===")
            print(f"Solvency Score: {insights.solvency_score}")
            print(f"Profitability Ratio: {insights.profitability_ratio}")
            print(f"Narrative Summary: {insights.narrative_summary}")
        else:
            logger.error("Analysis returned no insights.")

    except Exception as e:
        logger.exception(f"Unhandled exception occurred: {e}")

if __name__ == "__main__":
    main()
