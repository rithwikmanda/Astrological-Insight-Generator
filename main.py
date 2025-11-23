from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
from logic import get_zodiac_sign, generate_insight

app = FastAPI(title="Astrological Insight Generator")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    name: str
    birth_date: str  # Format: YYYY-MM-DD
    birth_time: str  # Format: HH:MM
    birth_place: str
    language: str = "English"

class InsightResponse(BaseModel):
    zodiac: str
    insight: str
    language: str

@app.post("/predict", response_model=InsightResponse)
async def predict_insight(user_input: UserInput):
    try:
        # Parse date
        b_date = datetime.strptime(user_input.birth_date, "%Y-%m-%d")
        
        # 1. Calculate Zodiac
        zodiac = get_zodiac_sign(b_date.day, b_date.month)
        
        # 2. Generate Insight (LLM Stub)
        insight_text = generate_insight(user_input.name, zodiac, user_input.language)
        
        # 3. Return Response
        return InsightResponse(
            zodiac=zodiac,
            insight=insight_text,
            language=user_input.language
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return FileResponse("index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)