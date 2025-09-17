from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import httpx
import random
from typing import List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Roblox Outfit Marketplace Backend",
    description="Backend service for Roblox AI Style Assistant game",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str = Field(..., description="User message to the NPC")

class ChatResponse(BaseModel):
    reply: str = Field(..., description="NPC's reply to the user")

class RecommendRequest(BaseModel):
    theme: str = Field(..., description="Theme for outfit recommendations")

class OutfitItem(BaseModel):
    assetId: int = Field(..., description="Roblox asset ID")
    type: str = Field(..., description="Type of outfit item")

class RecommendResponse(BaseModel):
    items: List[OutfitItem] = Field(..., description="List of recommended outfit items")

# NPC chat responses based on common themes
NPC_RESPONSES = {
    "greeting": [
        "Welcome to the Roblox Outfit Marketplace! I'm here to help you find the perfect style!",
        "Hey there! Ready to discover some amazing outfits? I've got tons of recommendations!",
        "Hello! I'm your AI Style Assistant. What kind of look are you going for today?"
    ],
    "recommendation": [
        "Based on your style preferences, I think you'll love these outfit suggestions!",
        "I've found some fantastic pieces that would look amazing on you!",
        "These items are trending right now and would be perfect for your style!"
    ],
    "default": [
        "That's interesting! I'm here to help you with outfit recommendations. What style are you looking for?",
        "I love talking about fashion! What kind of outfits are you interested in?",
        "Style is all about expressing yourself! What theme speaks to you today?"
    ]
}

# Sample outfit data since we can't access real Roblox API without authentication
SAMPLE_OUTFITS = {
    "casual": [
        {"assetId": 1234567890, "type": "shirt"},
        {"assetId": 2345678901, "type": "pants"},
        {"assetId": 3456789012, "type": "hat"},
        {"assetId": 4567890123, "type": "shoes"},
        {"assetId": 5678901234, "type": "accessory"},
        {"assetId": 6789012345, "type": "hair"}
    ],
    "formal": [
        {"assetId": 7890123456, "type": "shirt"},
        {"assetId": 8901234567, "type": "pants"},
        {"assetId": 9012345678, "type": "tie"},
        {"assetId": 1023456789, "type": "shoes"},
        {"assetId": 1134567890, "type": "jacket"},
        {"assetId": 1245678901, "type": "watch"}
    ],
    "sporty": [
        {"assetId": 1356789012, "type": "jersey"},
        {"assetId": 1467890123, "type": "shorts"},
        {"assetId": 1578901234, "type": "sneakers"},
        {"assetId": 1689012345, "type": "cap"},
        {"assetId": 1790123456, "type": "socks"},
        {"assetId": 1801234567, "type": "wristband"}
    ],
    "gothic": [
        {"assetId": 1912345678, "type": "shirt"},
        {"assetId": 2023456789, "type": "pants"},
        {"assetId": 2134567890, "type": "boots"},
        {"assetId": 2245678901, "type": "cape"},
        {"assetId": 2356789012, "type": "necklace"},
        {"assetId": 2467890123, "type": "mask"}
    ],
    "kawaii": [
        {"assetId": 2578901234, "type": "dress"},
        {"assetId": 2689012345, "type": "bow"},
        {"assetId": 2790123456, "type": "shoes"},
        {"assetId": 2801234567, "type": "bag"},
        {"assetId": 2912345678, "type": "hairpin"},
        {"assetId": 3023456789, "type": "socks"}
    ]
}

def get_npc_response(message: str) -> str:
    """Generate an appropriate NPC response based on the user's message."""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
        return random.choice(NPC_RESPONSES["greeting"])
    elif any(word in message_lower for word in ["recommend", "suggestion", "outfit", "style", "clothes"]):
        return random.choice(NPC_RESPONSES["recommendation"])
    else:
        return random.choice(NPC_RESPONSES["default"])

async def fetch_roblox_catalog_items(theme: str, limit: int = 8) -> List[OutfitItem]:
    """
    Fetch outfit items from Roblox catalog API.
    For now, using sample data. In production, this would make real API calls.
    """
    try:
        # In a real implementation, you would use the Roblox catalog API:
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(f"https://catalog.roblox.com/v1/search/items?category=Clothing&keyword={theme}&limit={limit}")
        #     data = response.json()
        #     return [OutfitItem(assetId=item["id"], type=item["itemType"]) for item in data["data"]]
        
        # Using sample data for demonstration
        theme_lower = theme.lower()
        outfit_items = []
        
        # Find matching theme or use a default
        if theme_lower in SAMPLE_OUTFITS:
            outfit_items = SAMPLE_OUTFITS[theme_lower]
        else:
            # Use casual as default and mix with other themes
            outfit_items = SAMPLE_OUTFITS["casual"][:4] + SAMPLE_OUTFITS["formal"][:2]
        
        # Shuffle and limit results
        random.shuffle(outfit_items)
        selected_items = outfit_items[:min(limit, len(outfit_items))]
        
        return [OutfitItem(**item) for item in selected_items]
        
    except Exception as e:
        logger.error(f"Error fetching catalog items: {e}")
        # Fallback to casual items
        fallback_items = SAMPLE_OUTFITS["casual"][:6]
        return [OutfitItem(**item) for item in fallback_items]

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Roblox Outfit Marketplace Backend",
        "description": "AI Style Assistant backend for Roblox game",
        "endpoints": {
            "/chat": "Chat with NPC for style advice",
            "/recommend": "Get outfit recommendations by theme"
        },
        "version": "1.0.0"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint where NPC replies to user prompts.
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        npc_reply = get_npc_response(request.message)
        
        logger.info(f"Chat request: {request.message[:50]}... -> Reply: {npc_reply[:50]}...")
        
        return ChatResponse(reply=npc_reply)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/recommend", response_model=RecommendResponse)
async def recommend(request: RecommendRequest):
    """
    Recommend endpoint that fetches 6-10 outfit items from Roblox catalog API by theme.
    Returns JSON with assetId and type.
    """
    try:
        if not request.theme.strip():
            raise HTTPException(status_code=400, detail="Theme cannot be empty")
        
        # Fetch outfit items (6-10 items)
        outfit_items = await fetch_roblox_catalog_items(request.theme, limit=random.randint(6, 10))
        
        if not outfit_items:
            raise HTTPException(status_code=404, detail="No outfit items found for this theme")
        
        logger.info(f"Recommendation request for theme '{request.theme}' -> {len(outfit_items)} items")
        
        return RecommendResponse(items=outfit_items)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in recommend endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)