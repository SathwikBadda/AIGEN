from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from src.services.codeAgent import CodeAssistant

app = FastAPI()

# Add required security headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

assistant = CodeAssistant()

@app.post("/api/analyze-code")
async def analyze_code(request: Request):
    try:
        body = await request.json()
        code = body.get("code", "")  # Default to empty string
        query = body.get("query")
        
        # Allow empty code if there's a query
        if not code and not query:
            raise HTTPException(status_code=400, detail="No code or query provided")
            
        result = assistant.analyze_code(code, query)
        return result
    except Exception as e:
        return {"status": "error", "response": str(e)}