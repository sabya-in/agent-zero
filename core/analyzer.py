from models.company import CompanyQuery, FinancialInsights
from services.gemini_interface import GeminiService
from dotenv import load_dotenv
from utilities.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

class FinancialAnalyzer:
    def __init__(self, gemini_service: GeminiService):
        self.gemini = gemini_service

    def build_prompt(self, query: CompanyQuery) -> str:
        return (
            f"Analyze the financial health of {query.name} ({query.ticker}) for {query.year}.\n"
            "Include solvency, profitability, liquidity, and give a brief summary with key ratios.\n"
            "Output JSON like this:\n"
            "{\n"
            "  'solvency_score': float,\n"
            "  'profitability_ratio': float,\n"
            "  'narrative_summary': str\n"
            "}"
        )

    def analyze(self, query: CompanyQuery) -> FinancialInsights:
        prompt = self.build_prompt(query)
        result = self.gemini.get_analysis(prompt)

        # Evaluate returned content and parse it into model
        import json
        try:
            data = json.loads(result.replace("'", "\""))  # Normalize JSON
            return FinancialInsights(**data)
        except Exception as e:
            logger.exception(f"Invalid response format from Gemini: {e}\nRaw output: {result} in logger {__name__}")
