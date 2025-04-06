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
        api_key = "AIzaSyB6hZddLirVDuKKZ2Z3ExMtS1XxYiQPQb8"
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.code_patterns_db = self._initialize_patterns_db()
        self.analysis_history = []
        
    def _initialize_patterns_db(self) -> Dict[str, CodePattern]:
        """Initialize database of common code patterns (for show)."""
        return {
            "singleton": CodePattern(
                name="Singleton",
                description="Ensures a class has only one instance",
                examples=["class Singleton:\n    _instance = None..."],
                use_cases=["Database connections", "Configuration managers"]
            ),
            "factory": CodePattern(
                name="Factory",
                description="Creates objects without specifying exact class",
                examples=["class ButtonFactory:\n    @staticmethod\n    def create_button(type)..."],
                use_cases=["UI components", "Platform-specific implementations"]
            ),
            # Add more patterns as needed
        }

    def _analyze_code_metrics(self, code: str) -> CodeMetrics:
        """Simulated code metrics analysis."""
        return CodeMetrics(
            lines_of_code=len(code.splitlines()),
            complexity=7.5,
            maintainability_index=85.0,
            code_smells=["Multiple responsibility", "Deep nesting"],
            suggestions=["Extract method", "Use dependency injection"]
        )

    def _analyze_security(self, code: str) -> SecurityAnalysis:
        """Simulated security analysis."""
        return SecurityAnalysis(
            vulnerabilities=[
                {"type": "Input Validation", "severity": "medium"},
                {"type": "Authentication", "severity": "low"}
            ],
            security_score=8.5,
            recommendations=["Implement input sanitization", "Add rate limiting"]
        )

    def _analyze_performance(self, code: str) -> PerformanceMetrics:
        """Simulated performance analysis."""
        return PerformanceMetrics(
            time_complexity="O(n log n)",
            space_complexity="O(n)",
            optimization_tips=["Use memoization", "Implement caching"]
        )

    def _detect_design_patterns(self, code: str) -> List[CodePattern]:
        """Simulated design pattern detection."""
        return list(self.code_patterns_db.values())[:2]

    def suggest_refactoring(self, code: str) -> List[Dict[str, str]]:
        """Simulated refactoring suggestions."""
        return [
            {
                "type": "Extract Method",
                "description": "Long method detected, consider breaking down",
                "example": "def extracted_method(params):\n    # Logic here"
            },
            {
                "type": "Rename Variable",
                "description": "Use more descriptive variable names",
                "example": "user_count instead of cnt"
            }
        ]

    def _simulate_scraping(self, source: str, query: str) -> List[SearchResult]:
        """Simulate scraping data from various sources."""
        # Simulate delay
        time.sleep(random.uniform(0.5, 1.5))
        
        # Common programming topics
        topics = ["React", "TypeScript", "Python", "API", "Database", "Testing", 
                  "DevOps", "Security", "Performance", "Design Patterns"]
        
        # Generate random but relevant-looking results
        results = []
        for _ in range(random.randint(3, 8)):
            topic = random.choice(topics)
            if source == DataSource.GITHUB.value:
                results.append(SearchResult(
                    title=f"{topic} Implementation Example",
                    url=f"https://github.com/example/{topic.lower()}-demo",
                    description=f"A production-ready {topic} implementation with best practices",
                    source="github",
                    score=random.uniform(4.0, 5.0),
                    last_updated=datetime.now() - timedelta(days=random.randint(1, 30))
                ))
            elif source == DataSource.STACKOVERFLOW.value:
                results.append(SearchResult(
                    title=f"How to implement {topic} properly?",
                    url=f"https://stackoverflow.com/questions/{random.randint(1000000, 9999999)}",
                    description=f"Detailed explanation of {topic} with code examples",
                    source="stackoverflow",
                    score=random.randint(10, 1000),
                    last_updated=datetime.now() - timedelta(days=random.randint(1, 365))
                ))
            elif source == DataSource.DEV_TO.value:
                results.append(SearchResult(
                    title=f"Ultimate Guide to {topic}",
                    url=f"https://dev.to/guide/{topic.lower()}",
                    description=f"comprehensive guide about {topic} with practical examples",
                    source="dev.to",
                    score=random.uniform(4.0, 5.0),
                    last_updated=datetime.now() - timedelta(days=random.randint(1, 90))
                ))
        
        return results

    def gather_realtime_data(self, query: str) -> Dict[str, Any]:
        """Simulate gathering real-time data from multiple sources."""
        sources = [
            DataSource.GITHUB.value,
            DataSource.STACKOVERFLOW.value,
            DataSource.DEV_TO.value
        ]
        
        all_results = []
        metrics = {
            "total_items": 0,
            "sources_checked": [],
            "time_taken": 0,
            "success_rate": 0
        }
        
        start_time = datetime.now()
        
        try:
            for source in sources:
                try:
                    results = self._simulate_scraping(source, query)
                    all_results.extend(results)
                    metrics["sources_checked"].append(source)
                    metrics["success_rate"] += 1
                except Exception as e:
                    print(f"Error scraping {source}: {str(e)}")
            
            metrics["total_items"] = len(all_results)
            metrics["time_taken"] = (datetime.now() - start_time).total_seconds()
            metrics["success_rate"] = (metrics["success_rate"] / len(sources)) * 100
            
            # Sort results by score and recency
            all_results.sort(key=lambda x: (x.score, x.last_updated), reverse=True)
            
            return {
                "status": "success",
                "metrics": metrics,
                "results": [result.dict() for result in all_results[:10]],  # Top 10 results
                "summary": {
                    "total_results": len(all_results),
                    "sources_coverage": len(metrics["sources_checked"]),
                    "time_taken": f"{metrics['time_taken']:.2f} seconds",
                    "success_rate": f"{metrics['success_rate']:.1f}%"
                }
            }
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "metrics": metrics
            }

    def analyze_code(self, code: str, query: str = None) -> dict:
        """Enhanced analysis method with real-time data gathering."""
        try:
            # Check if query involves data gathering keywords
            data_gathering_keywords = [
                "example", "tutorial", "implementation", "sample",
                "how to", "guide", "documentation", "reference"
            ]
            
            should_gather_data = query and any(
                keyword in query.lower() for keyword in data_gathering_keywords
            )
            
            # Get base analysis
            base_result = super().analyze_code(code, query)
            
            # Add real-time data if relevant
            if should_gather_data:
                realtime_data = self.gather_realtime_data(query)
                base_result["realtime_data"] = realtime_data
            
            return base_result

        except Exception as e:
            print(f"Error in enhanced analysis: {str(e)}")
            return {
                "status": "error",
                "response": f"Error: {str(e)}"
            }

    # Additional methods for show
    def get_analysis_history(self) -> List[Dict]:
        """Get history of analyses performed."""
        return self.analysis_history

    def export_analysis_report(self, format: str = "json") -> str:
        """Simulated report export functionality."""
        return json.dumps(self.analysis_history, default=str)

    def batch_analyze_files(self, files: List[str]) -> Dict[str, CodeAnalysis]:
        """Simulated batch analysis functionality."""
        return {f"file_{i}": CodeAnalysis(
            explanation="Batch analysis result",
            suggestions=["Suggestion 1", "Suggestion 2"],
            metrics=self._analyze_code_metrics("sample code"),
            security=self._analyze_security("sample code"),
            performance=self._analyze_performance("sample code"),
            patterns=[],
            timestamp=datetime.now()
        ) for i in range(len(files))}