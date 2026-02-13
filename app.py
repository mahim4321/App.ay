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
import React, { useState } from 'react';

const AdvancedChatApp = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! Ami Gemini 3 Flash. Kivabe sahayyo korte pari?", sender: "ai" }
  ]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { id: Date.now(), text: input, sender: "user" }]);
      setInput("");
      // Ekhane AI API call korar logic thakbe
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black text-white p-4 flex flex-col items-center">
      {/* Header */}
      <div className="w-full max-w-2xl flex justify-between items-center mb-8 p-4 bg-white/10 backdrop-blur-md rounded-2xl border border-white/20">
        <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          Gemini 3 Pro AI
        </h1>
        <div className="h-3 w-3 bg-green-500 rounded-full animate-pulse"></div>
      </div>

      {/* Chat Window */}
      <div className="w-full max-w-2xl h-[60vh] overflow-y-auto space-y-4 p-4 scrollbar-hide">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-4 rounded-2xl ${
              msg.sender === 'user' 
              ? 'bg-blue-600 text-white rounded-tr-none' 
              : 'bg-white/10 backdrop-blur-sm border border-white/10 rounded-tl-none'
            }`}>
              {msg.text}
            </div>
          </div>
        ))}
      </div>

      {/* Input Field */}
      <div className="w-full max-w-2xl mt-6 relative">
        <input 
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything..."
          className="w-full p-5 bg-white/5 border border-white/20 rounded-3xl focus:outline-none focus:ring-2 focus:ring-blue-500 backdrop-blur-xl"
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        />
        <button 
          onClick={handleSend}
          className="absolute right-3 top-3 bg-blue-500 hover:bg-blue-600 p-3 rounded-2xl transition-all"
        >
          🚀
        </button>
      </div>
    </div>
  );
};

export default AdvancedChatApp;
