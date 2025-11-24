from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from datetime import datetime
from logic import get_zodiac_sign, generate_insight_stream, get_vedic_details

app = FastAPI(title="Astrological Insight Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    name: str
    birth_date: str
    birth_time: str
    birth_place: str
    language: str = "English"
    category: str = "General"

class CalculationResponse(BaseModel):
    zodiac: str
    vedic: dict

# Endpoint 1: Calculate Data
@app.post("/calculate", response_model=CalculationResponse)
async def calculate_data(user_input: UserInput):
    try:
        b_date = datetime.strptime(user_input.birth_date, "%Y-%m-%d")
        zodiac = get_zodiac_sign(b_date.day, b_date.month)
        vedic_data = get_vedic_details(b_date, user_input.birth_time, user_input.birth_place)
        return CalculationResponse(zodiac=zodiac, vedic=vedic_data)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format.")

# Endpoint 2: Stream Text
@app.post("/stream_insight")
async def stream_insight(user_input: UserInput):
    try:
        b_date = datetime.strptime(user_input.birth_date, "%Y-%m-%d")
        zodiac = get_zodiac_sign(b_date.day, b_date.month)
        vedic_data = get_vedic_details(b_date, user_input.birth_time, user_input.birth_place)
        
        return StreamingResponse(
            generate_insight_stream(
                user_input.name, 
                zodiac, 
                user_input.category, 
                user_input.language, 
                vedic_data
            ),
            media_type="text/plain"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    return FileResponse("index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
