from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os
import uvicorn
from typing import Dict, Any

# Initialize FastAPI app
app = FastAPI(title="Zoho Cliq ChatGPT Bot")

# Set OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

class CliqMessage(BaseModel):
    text: str = ""

@app.post("/cliq-chat")
async def cliq_chat(request: Request):
    """Endpoint for Zoho Cliq bot - receives message, sends to ChatGPT, returns response"""
    try:
        data = await request.json()
        user_message = data.get("text", "")
        
        if not user_message:
            return {"text": "Please send a message!"}
        
        # Call OpenAI ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful assistant integrated with Zoho Cliq. Keep responses concise and professional."
                },
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        reply = response.choices[0].message.content.strip()
        return {"text": reply}
        
    except Exception as e:
        return {"text": f"Sorry, I encountered an error: {str(e)[:100]}..."}

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {"status": "Zoho Cliq ChatGPT Bot is running!", "endpoint": "/cliq-chat"}

@app.get("/docs")
async def docs():
    return {"docs": "Visit http://localhost:8000/docs for interactive API docs"}
