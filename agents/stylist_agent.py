"""
Stylist agent for providing fashion advice and style recommendations.
This agent specializes in understanding user preferences and translating them into style advice.
"""

from typing import Union
from .contracts import ChatIn, ChatOut, RecommendIn, TagSpec


class StylistAgent:
    """
    Stylist agent class for converting natural language prompts to TagSpec.
    Uses deterministic keyword detection for stable frontend tests.
    """
    
    def __init__(self):
        """Initialize the StylistAgent with keyword mappings."""
        # Theme keywords mapping - order matters for precedence
        self.theme_keywords = {
            "knight": ["knight", "armor", "medieval warrior", "chivalry"],
            "medieval": ["medieval", "middle ages", "castle", "feudal"],
            "futuristic": ["futuristic", "cyberpunk", "sci-fi", "space", "tech", "neon"],
            "formal": ["formal", "professional", "business", "elegant"],
            "casual": ["casual", "everyday", "comfortable", "relaxed"],
            "sporty": ["sporty", "athletic", "active", "sport"],
            "gothic": ["gothic", "dark", "alternative", "goth"],
            "kawaii": ["kawaii", "cute", "colorful", "adorable"]
        }
        
        # Vibe keywords - can be combined with themes
        self.vibe_keywords = {
            "futuristic": ["futuristic", "cyberpunk", "sci-fi", "space", "tech", "neon"],
            "dramatic": ["dramatic", "gothic", "dark", "intense"],
            "playful": ["playful", "kawaii", "cute", "fun", "colorful"],
            "professional": ["professional", "formal", "business"],
            "relaxed": ["relaxed", "casual", "comfortable"],
            "active": ["active", "sporty", "athletic"]
        }
        
        # Default parts as specified in the issue
        self.default_parts = [
            "Head", "Face", "Torso", "Left Arm", "Right Arm", 
            "Pants", "Shirt", "Back Accessory"
        ]
    
    def run(self, prompt: str) -> TagSpec:
        """
        Convert a natural language prompt to a TagSpec.
        
        Args:
            prompt: User's natural language prompt describing desired style
            
        Returns:
            TagSpec with detected theme, optional vibe, and default parts
        """
        prompt_lower = prompt.lower()
        
        # Detect theme (first match wins for deterministic behavior)
        detected_theme = None
        for theme, keywords in self.theme_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                detected_theme = theme
                break
        
        # Default theme if none detected
        if not detected_theme:
            detected_theme = "casual"
        
        # Detect vibe (independent of theme detection)
        detected_vibe = None
        for vibe, keywords in self.vibe_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                # Special case: if theme is detected as the same as vibe, don't set vibe
                if vibe != detected_theme:
                    detected_vibe = vibe
                    break
        
        return TagSpec(
            theme=detected_theme,
            vibe=detected_vibe,
            budget=None,  # No budget specified by default
            parts=self.default_parts
        )


def run(input_data: Union[ChatIn, RecommendIn]) -> Union[ChatOut, TagSpec]:
    """
    Run the stylist agent with the given input.
    
    Args:
        input_data: Either ChatIn or RecommendIn contract
        
    Returns:
        Either ChatOut for chat interactions or TagSpec for style specifications
    """
    if isinstance(input_data, ChatIn):
        # Handle style advice chat
        prompt_lower = input_data.prompt.lower()
        
        if any(word in prompt_lower for word in ["formal", "professional", "business"]):
            reply = "For a formal look, I'd recommend elegant pieces with clean lines and sophisticated colors!"
        elif any(word in prompt_lower for word in ["casual", "everyday", "comfortable"]):
            reply = "Casual style is all about comfort and versatility. Think relaxed fits and easy-to-mix pieces!"
        elif any(word in prompt_lower for word in ["sporty", "athletic", "active"]):
            reply = "Sporty vibes call for functional yet stylish pieces that move with you!"
        elif any(word in prompt_lower for word in ["gothic", "dark", "alternative"]):
            reply = "Gothic style embraces darker aesthetics with dramatic silhouettes and bold accessories!"
        elif any(word in prompt_lower for word in ["kawaii", "cute", "colorful"]):
            reply = "Kawaii style is all about embracing cuteness with bright colors and playful elements!"
        else:
            reply = "I'm here to help you discover your perfect style! What kind of vibe are you going for?"
        
        return ChatOut(
            success=True,
            user_id=input_data.user_id,
            reply=reply
        )
    
    elif isinstance(input_data, RecommendIn):
        # Convert theme to styling specification
        theme = input_data.theme.lower()
        
        # Generate vibe and styling suggestions based on theme
        vibe_mapping = {
            "formal": "professional",
            "casual": "relaxed", 
            "sporty": "active",
            "gothic": "dramatic",
            "kawaii": "playful"
        }
        
        parts_mapping = {
            "formal": ["shirt", "pants", "shoes", "tie", "jacket"],
            "casual": ["shirt", "pants", "shoes", "hat"],
            "sporty": ["jersey", "shorts", "sneakers", "cap"],
            "gothic": ["shirt", "pants", "boots", "cape", "accessories"],
            "kawaii": ["dress", "bow", "shoes", "bag", "accessories"]
        }
        
        vibe = vibe_mapping.get(theme, "stylish")
        parts = parts_mapping.get(theme, ["shirt", "pants", "shoes", "accessories"])
        
        return TagSpec(
            theme=input_data.theme,
            vibe=vibe,
            budget=None,  # No budget specified by default
            parts=parts
        )
    
    else:
        raise ValueError(f"Unsupported input type: {type(input_data)}")