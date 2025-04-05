from pydantic import BaseModel, Field
from typing import List
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class CodeAnalysis(BaseModel):
    explanation: str
    suggestions: List[str]

class CodeAssistant:
    def __init__(self):
        api_key = "AIzaSyB6hZddLirVDuKKZ2Z3ExMtS1XxYiQPQb8"
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def analyze_code(self, code: str, query: str = None) -> dict:
        """Provides code analysis and answers questions."""
        try:
            # Handle general questions without code
            if not code.strip() and query:
                prompt = f"""
                Programming Question: {query}
                Please provide a detailed and helpful response, using code examples where appropriate.
                """
            else:
                # Handle code analysis with or without specific questions
                if code.strip():
                    if query:
                        prompt = f"""
                        Analyze this code and answer the question:
                        ```python
                        {code}
                        ```
                        
                        Question: {query}
                        Please provide a detailed response focusing on the code shown above.
                        """
                    else:
                        prompt = f"""
                        Please analyze this code and explain what it does:
                        ```python
                        {code}
                        ```
                        Focus on the main functionality, important components, and potential improvements.
                        """
                else:
                    return {
                        "status": "error",
                        "response": "Please provide code to analyze or ask a question."
                    }
            
            response = self.model.generate_content(prompt)
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