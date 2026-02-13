import os
from fastapi import FastAPI, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient # MongoDB Async Driver
from pydantic import BaseModel
from google import genai

app = FastAPI()

# --- 1. Database Connection ---
MONGO_URL = "mongodb://localhost:27017" # Apnar MongoDB link
client_db = AsyncIOMotorClient(MONGO_URL)
db = client_db.my_advance_app

# --- 2. AI Setup ---
ai_client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

# --- 3. Data Schema ---
class ChatRequest(BaseModel):
    user_id: str
    message: str

# --- 4. Advanced Logic Endpoint ---
@app.post("/api/v1/chat")
async def handle_chat(request: ChatRequest):
    # Step A: User-er message Database-e save kora
    await db.history.insert_one({
        "user_id": request.user_id,
        "message": request.message,
        "role": "user"
    })

    # Step B: Gemini 3 Flash theke response neya
    try:
        response = ai_client.models.generate_content(
            model="gemini-3-flash",
            contents=request.message
        )
        ai_reply = response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail="AI Service Error")

    # Step C: AI response-o save kora (History-r jonno)
    await db.history.insert_one({
        "user_id": request.user_id,
        "message": ai_reply,
        "role": "assistant"
    })

    return {"status": "success", "reply": ai_reply}
