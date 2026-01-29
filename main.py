from fastapi import FastAPI, Request
import openai
import os

app = FastAPI(docs_url=None, redoc_url=None)

# Global API key (works with ANY openai version)
openai.api_key = os.getenv("OPENAI_API_KEY") 

@app.post("/cliq-chat")
async def cliq_chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("text", "")
        
        if not user_message:
            return {"text": "Please send a message!"}
        
        # Direct call - NO client object needed
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful Zoho Cliq assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500
        )
        
        reply = response.choices[0].message.content.strip()
        return {"text": reply}
        
    except Exception as e:
        return {"text": f"Error: {str(e)[:100]}..."}

@app.get("/")
async def health():
    return {"status": "Zoho Cliq bot running"}
