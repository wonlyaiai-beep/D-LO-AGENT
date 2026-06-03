import asyncio
import uuid
from groq import Groq
from config import GROQ_API_KEY, PRIMARY_MODEL, FALLBACK_MODEL, MAX_RETRIES
from prompts import SYSTEM_PROMPT
from memory import save_message, get_history
from tools import send_lead_email

client = Groq(api_key=GROQ_API_KEY)

async def get_response(session_id, user_message):
    """Agent response lo — reliability + fallback ke saath"""
    
    # History lo
    history = get_history(session_id)
    
    # Messages banao
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    messages.append({"role": "user", "content": user_message})
    
    # Retry logic
    for attempt in range(MAX_RETRIES):
        try:
            model = PRIMARY_MODEL if attempt == 0 else FALLBACK_MODEL
            
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            reply = response.choices[0].message.content
            
            # History save karo
            save_message(session_id, "user", user_message)
            save_message(session_id, "assistant", reply)
            
            # Lead detect karo
            lead_keywords = [
                "call karenge", "schedule", 
                "contact number", "0333", "03",
                "call schedule", "jald hi call"
            ]
            
            if any(keyword in reply.lower() for keyword in lead_keywords):
                lead_data = {
                    "naam": "New Lead",
                    "business": "Unknown",
                    "masla": user_message,
                    "contact": "Check conversation",
                    "summary": f"User: {user_message}\nAgent: {reply}"
                }
                send_lead_email(lead_data)
                print("📧 Lead email bhej di! ✅")
            
            return reply
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == MAX_RETRIES - 1:
                return "Maafi chahta hun — abhi technical masla hai. Thodi der mein dobara try karein! 🙏"
    
    return "Kuch masla aa gaya — please dobara try karein!"