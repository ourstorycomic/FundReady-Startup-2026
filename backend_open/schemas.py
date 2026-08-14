from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class DocumentAnalysisRequest(BaseModel):
    document_type: str = "pitchdeck"
    content: str

class FundingAllocationItem(BaseModel):
    category: str
    percentage: str
    amount: str
    objective: str

class SystemRecommendation(BaseModel):
    desired_amount: str
    recommended_amount: str
    difference: str
    rationale: str

class ScenarioOption(BaseModel):
    name: str
    allocation: List[FundingAllocationItem]
    focus: str
    expected_result: str

class InvestmentDetail(BaseModel):
    category: str
    amount: str
    why_invest: str
    to_solve: List[str]
    expected_result: str

class ComparisonRow(BaseModel):
    category: str
    scenario_a: str
    scenario_b: str

class DetailedSection(BaseModel):
    title: str
    content: str

class FundingScenario(BaseModel):
    current_desire: str
    recommendation: SystemRecommendation
    scenarios: List[ScenarioOption]
    investment_details: List[InvestmentDetail]
    comparison_rationale: str
    comparison_table: List[ComparisonRow]
    final_advice: str
    detailed_sections: Optional[List[DetailedSection]] = None

class ScoreBreakdown(BaseModel):
    name: str
    score: int
    maximum: int
    reason: str

class ScoreResponse(BaseModel):
    score: int
    max_score: int
    grade: str
    breakdown: List[ScoreBreakdown] = []
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    funding_scenario: Optional[FundingScenario] = None

class FinancialCalculationRequest(BaseModel):
    revenue: float
    gross_margin: float
    roe: float
    current_ratio: float
    debt_to_equity: float
    cash_flow_margin: float

class MatcherRequest(BaseModel):
    description: str
    top_n: int = Field(default=3)

class FullAssessmentRequest(BaseModel):
    documents: Dict[str, str]
    financials: Optional[Dict[str, Any]] = None
