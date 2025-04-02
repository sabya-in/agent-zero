from pydantic import BaseModel

class CompanyQuery(BaseModel):
    name: str
    ticker: str
    year: int

class FinancialInsights(BaseModel):
    solvency_score: float
    profitability_ratio: float
    narrative_summary: str
