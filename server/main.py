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
    prompt: str = Field(..., description="User prompt to the NPC")
    user_id: int = Field(..., description="User ID")

class ChatResponse(BaseModel):
    success: bool = Field(..., description="Whether the request was successful")
    user_id: int = Field(..., description="User ID")
    reply: str = Field(..., description="NPC's reply to the user")

class RecommendRequest(BaseModel):
    theme: str = Field(..., description="Theme for outfit recommendations")
    user_id: int = Field(..., description="User ID")

class OutfitItem(BaseModel):
    assetId: str = Field(..., description="Roblox asset ID as string")
    type: str = Field(..., description="Type of outfit item")

class RecommendResponse(BaseModel):
    success: bool = Field(..., description="Whether the request was successful")
    user_id: int = Field(..., description="User ID")
    message: str = Field(..., description="Outfit ready message")
    outfit: List[OutfitItem] = Field(..., description="List of recommended outfit items")

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

def get_npc_response(prompt: str) -> str:
    """Generate an appropriate NPC response based on the user's prompt."""
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ["hello", "hi", "hey", "greetings"]):
        return random.choice(NPC_RESPONSES["greeting"])
    elif any(word in prompt_lower for word in ["recommend", "suggestion", "outfit", "style", "clothes"]):
        return random.choice(NPC_RESPONSES["recommendation"])
    else:
        return random.choice(NPC_RESPONSES["default"])

async def fetch_roblox_catalog_items(theme: str, limit: int = 10) -> List[OutfitItem]:
    """
    Fetch outfit items from Roblox catalog API v2.
    Uses the search/items/details endpoint with retry logic.
    Falls back to sample data if API is unavailable.
    """
    url = "https://catalog.roblox.com/v2/search/items/details"
    params = {
        "categoryFilter": "CommunityCreations",
        "limit": min(limit, 10),  # Cap at 10 as per requirements
        "keyword": theme
    }
    
    # Retry configuration
    max_retries = 3
    timeout = 10.0
    
    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                logger.info(f"Fetching Roblox catalog items for theme '{theme}', attempt {attempt + 1}")
                response = await client.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                # Validate response structure
                if "data" not in data or not isinstance(data["data"], list):
                    logger.warning(f"Invalid response structure from Roblox API: {data}")
                    raise ValueError("Invalid response structure")
                
                items = []
                for item in data["data"]:
                    # Extract assetId and type from the item
                    asset_id = str(item.get("id", ""))
                    item_type = item.get("itemType", "") or item.get("assetType", "Accessory")
                    
                    if asset_id:  # Only add items with valid IDs
                        items.append(OutfitItem(assetId=asset_id, type=item_type))
                
                logger.info(f"Successfully fetched {len(items)} items for theme '{theme}'")
                return items[:limit]  # Ensure we don't exceed the limit
                
        except httpx.HTTPStatusError as e:
            logger.warning(f"HTTP error on attempt {attempt + 1}: {e.response.status_code}")
            if attempt == max_retries - 1:
                break
        except httpx.TimeoutException:
            logger.warning(f"Timeout on attempt {attempt + 1}")
            if attempt == max_retries - 1:
                break
        except Exception as e:
            logger.warning(f"Error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                break
    
    # Fallback to sample data if API is unavailable
    logger.warning(f"Roblox API unavailable, using sample data for theme '{theme}'")
    return get_sample_outfit_items(theme, limit)


def get_sample_outfit_items(theme: str, limit: int) -> List[OutfitItem]:
    """
    Get sample outfit items when the real API is unavailable.
    Converts sample data to match the new string-based assetId format.
    """
    theme_lower = theme.lower()
    
    # Find matching theme or use a default
    if theme_lower in SAMPLE_OUTFITS:
        outfit_items = SAMPLE_OUTFITS[theme_lower]
    else:
        # Use casual as default and mix with other themes for variety
        outfit_items = SAMPLE_OUTFITS["casual"][:4] + SAMPLE_OUTFITS["formal"][:2]
    
    # Shuffle and limit results
    random.shuffle(outfit_items)
    selected_items = outfit_items[:min(limit, len(outfit_items))]
    
    # Convert to OutfitItem objects with string assetIds
    return [OutfitItem(assetId=str(item["assetId"]), type=item["type"]) for item in selected_items]

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
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        npc_reply = get_npc_response(request.prompt)
        
        logger.info(f"Chat request from user {request.user_id}: {request.prompt[:50]}... -> Reply: {npc_reply[:50]}...")
        
        return ChatResponse(
            success=True,
            user_id=request.user_id,
            reply=npc_reply
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/recommend", response_model=RecommendResponse)
async def recommend(request: RecommendRequest):
    """
    Recommend endpoint that fetches 6-10 outfit items from Roblox catalog API by theme.
    Returns JSON with assetId and type, plus success message.
    """
    try:
        if not request.theme.strip():
            raise HTTPException(status_code=400, detail="Theme cannot be empty")
        
        # Fetch outfit items (6-10 items)
        limit = random.randint(6, 10)
        outfit_items = await fetch_roblox_catalog_items(request.theme, limit=limit)
        
        if not outfit_items:
            # Return error response as per requirements
            return RecommendResponse(
                success=False,
                user_id=request.user_id,
                message=f"No items found for theme '{request.theme}'. Try a different theme.",
                outfit=[]
            )
        
        logger.info(f"Recommendation request from user {request.user_id} for theme '{request.theme}' -> {len(outfit_items)} items")
        
        return RecommendResponse(
            success=True,
            user_id=request.user_id,
            message=f"Your {request.theme} outfit is ready!",
            outfit=outfit_items
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in recommend endpoint: {e}")
        # For unexpected errors, still try to return a fallback response
        try:
            fallback_items = get_sample_outfit_items(request.theme, random.randint(6, 10))
            logger.info(f"Using fallback data for user {request.user_id}, theme '{request.theme}'")
            return RecommendResponse(
                success=True,
                user_id=request.user_id,
                message=f"Your {request.theme} outfit is ready!",
                outfit=fallback_items
            )
        except Exception:
            # If even fallback fails, return 502 as per requirements
            raise HTTPException(
                status_code=502, 
                detail="Failed to fetch outfit recommendations. Please try again later."
            )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)