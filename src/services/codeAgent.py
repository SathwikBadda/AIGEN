from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import random
import google.generativeai as genai
import os
from dotenv import load_dotenv
from enum import Enum
import json
import ast
import re
import time

load_dotenv()

class CodeLanguage(Enum):
    PYTHON = "python"
    TYPESCRIPT = "typescript"
    JAVASCRIPT = "javascript"
    REACT = "react"
    HTML = "html"
    CSS = "css"

class CodeAnalysisLevel(Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

@dataclass
class ScrapedData:
    source: str
    timestamp: datetime
    data: Any
    metadata: Dict[str, Any]

class DataSource(Enum):
    GITHUB = "github"
    STACKOVERFLOW = "stackoverflow"
    NPM = "npm"
    PYPI = "pypi"
    DEV_TO = "dev.to"
    MEDIUM = "medium"

class CodeMetrics(BaseModel):
    lines_of_code: int
    complexity: float
    maintainability_index: float
    code_smells: List[str]
    suggestions: List[str]

class SecurityAnalysis(BaseModel):
    vulnerabilities: List[Dict[str, str]]
    security_score: float
    recommendations: List[str]

class PerformanceMetrics(BaseModel):
    time_complexity: str
    space_complexity: str
    optimization_tips: List[str]

class CodePattern(BaseModel):
    name: str
    description: str
    examples: List[str]
    use_cases: List[str]

class ScrapingMetrics(BaseModel):
    total_items: int
    sources_checked: List[str]
    time_taken: float
    success_rate: float

class SearchResult(BaseModel):
    title: str
    url: str
    description: str
    source: str
    score: float
    last_updated: datetime

class CodeAnalysis(BaseModel):
    explanation: str
    suggestions: List[str]
    metrics: Optional[CodeMetrics]
    security: Optional[SecurityAnalysis]
    performance: Optional[PerformanceMetrics]
    patterns: List[CodePattern]
    timestamp: datetime

class CodeAssistant:
    def __init__(self):
        api_key = ""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def analyze_code(self, code: str = None, query: str = None) -> dict:
        """
        Handles both code analysis and general queries.
        
        Args:
            code (str, optional): Code to analyze
            query (str, optional): Question or query about the code/general programming
        """
        try:
            if code and query:
                # Code-specific analysis
                prompt = f"""
                Code to analyze:
                ```
                {code}
                ```
                Query: {query}
                Please provide a detailed response.
                """
            elif query:
                # General programming query
                prompt = f"Query: {query}\nPlease provide a detailed response."
            else:
                return {
                    "status": "error",
                    "response": "Either code or query must be provided"
                }

            # Generate response using Gemini model
            response = self.model.generate_content(prompt)
            return {
                "status": "success",
                "response": response.text
            }

        except Exception as e:
            print(f"Error in analysis: {str(e)}")
            return {
                "status": "error",
                "response": f"Analysis failed: {str(e)}"
            }
        
# ...existing code up to CodeAssistant class...

class CodeAnalyticsService:
    """Handles demo analytics, metrics, and web scraping functionality"""
    
    def __init__(self):
        self.analysis_history = []
        self.data_sources = {
            DataSource.GITHUB: "https://api.github.com",
            DataSource.STACKOVERFLOW: "https://api.stackexchange.com",
            DataSource.NPM: "https://registry.npmjs.org",
            DataSource.PYPI: "https://pypi.org/pypi",
            DataSource.DEV_TO: "https://dev.to/api",
            DataSource.MEDIUM: "https://api.medium.com"
        }

    def generate_demo_metrics(self, code: str) -> CodeMetrics:
        """Generate demo code quality metrics"""
        return CodeMetrics(
            lines_of_code=len(code.splitlines()),
            complexity=round(random.uniform(1.0, 10.0), 2),
            maintainability_index=round(random.uniform(60.0, 100.0), 2),
            code_smells=["Deep nesting", "Long method", "Duplicate code"],
            suggestions=["Extract method", "Use dependency injection", "Add error handling"]
        )

    def generate_demo_security(self, code: str) -> SecurityAnalysis:
        """Generate demo security analysis"""
        return SecurityAnalysis(
            vulnerabilities=[
                {"type": "SQL Injection", "severity": "high"},
                {"type": "XSS", "severity": "medium"},
                {"type": "CSRF", "severity": "low"}
            ],
            security_score=round(random.uniform(7.0, 9.9), 2),
            recommendations=[
                "Use parameterized queries",
                "Implement input validation",
                "Add rate limiting"
            ]
        )

    def generate_demo_performance(self, code: str) -> PerformanceMetrics:
        """Generate demo performance metrics"""
        return PerformanceMetrics(
            time_complexity="O(n log n)",
            space_complexity="O(n)",
            optimization_tips=[
                "Use memoization for recursive calls",
                "Implement caching",
                "Optimize database queries"
            ]
        )

    def simulate_web_scraping(self, query: str, sources: List[DataSource] = None) -> List[SearchResult]:
        """Simulate scraping multiple platforms for code examples and discussions"""
        if sources is None:
            sources = list(DataSource)

        results = []
        for source in sources:
            # Simulate delay for realism
            time.sleep(0.5)
            
            # Generate demo results
            results.extend([
                SearchResult(
                    title=f"Example {i+1} from {source.value}",
                    url=f"{self.data_sources[source]}/example{i+1}",
                    description=f"Related code example or discussion about {query}",
                    source=source.value,
                    score=round(random.uniform(0.5, 1.0), 2),
                    last_updated=datetime.now() - timedelta(days=random.randint(1, 30))
                )
                for i in range(3)
            ])

        return sorted(results, key=lambda x: x.score, reverse=True)

    def get_comprehensive_analysis(self, code: str, query: str = None) -> dict:
        """Generate comprehensive code analysis with metrics and scraped data"""
        try:
            metrics = self.generate_demo_metrics(code)
            security = self.generate_demo_security(code)
            performance = self.generate_demo_performance(code)
            
            # Simulate web scraping for related content
            scraped_data = self.simulate_web_scraping(query or "code patterns")
            
            analysis = CodeAnalysis(
                explanation="Detailed analysis of code structure and patterns",
                suggestions=[
                    "Implement error handling",
                    "Add input validation",
                    "Improve documentation"
                ],
                metrics=metrics,
                security=security,
                performance=performance,
                patterns=[
                    CodePattern(
                        name="Factory Pattern",
                        description="Creates objects without exposing creation logic",
                        examples=["class Factory:\n    def create(self):..."],
                        use_cases=["UI Components", "Database Connections"]
                    )
                ],
                timestamp=datetime.now()
            )

            result = {
                "status": "success",
                "analysis": analysis.dict(),
                "related_resources": [r.dict() for r in scraped_data[:5]],
                "scraping_metrics": ScrapingMetrics(
                    total_items=len(scraped_data),
                    sources_checked=[s.value for s in DataSource],
                    time_taken=random.uniform(0.5, 2.0),
                    success_rate=0.95
                ).dict()
            }

            self.analysis_history.append(result)
            return result

        except Exception as e:
            return {
                "status": "error",
                "response": f"Analysis failed: {str(e)}"
            }

    def get_analysis_history(self) -> List[dict]:
        """Get history of all analyses performed"""
        return self.analysis_history

    def export_report(self, format: str = "json") -> Union[str, dict]:
        """Export analysis history in specified format"""
        if format == "json":
            return {
                "analyses": self.analysis_history,
                "generated_at": datetime.now().isoformat(),
                "total_analyses": len(self.analysis_history)
            }
        return "Unsupported format"
