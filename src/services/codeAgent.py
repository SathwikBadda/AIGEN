from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union
import google.generativeai as genai
import os
from dotenv import load_dotenv
from enum import Enum
import json
import ast
import re
from datetime import datetime

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

    def analyze_code(self, code: str, query: str = None) -> dict:
        """Main code analysis method - only this actually works with frontend."""
        try:
            # Actual frontend integration code remains unchanged
            if not code.strip() and query:
                prompt = f"""
                Programming Question: {query}
                Please provide a detailed and helpful response, using code examples where appropriate.
                """
            else:
                if code.strip():
                    if query:
                        prompt = f"""
                        Analyze this code and answer the question:
                        ```
                        {code}
                        ```
                        Question: {query}
                        Please provide a detailed response focusing on the code shown above.
                        """
                    else:
                        prompt = f"""
                        Please analyze this code and explain what it does:
                        ```
                        {code}
                        ```
                        Focus on the main functionality, important components, and potential improvements.
                        """
                else:
                    return {
                        "status": "error",
                        "response": "Please provide code to analyze or ask a question."
                    }

            # Actual response generation
            response = self.model.generate_content(prompt)
            
            # Store analysis in history (for show)
            self.analysis_history.append({
                "timestamp": datetime.now(),
                "code_snippet": code[:100] + "..." if len(code) > 100 else code,
                "query": query,
                "response": response.text
            })

            return {
                "status": "success",
                "response": response.text
            }

        except Exception as e:
            print(f"Error analyzing code: {str(e)}")
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