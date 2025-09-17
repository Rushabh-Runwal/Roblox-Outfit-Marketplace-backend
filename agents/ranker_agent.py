"""
Ranker agent for scoring and ranking outfit recommendations.
This agent evaluates and sorts outfit items based on various criteria.
"""

from typing import List, Tuple, Union
import random
from .contracts import CatalogItem, TagSpec, RecommendOut


def run(input_data: Union[List[CatalogItem], Tuple[List[CatalogItem], TagSpec]]) -> Union[List[CatalogItem], RecommendOut]:
    """
    Run the ranker agent with the given input.
    
    Args:
        input_data: Either a list of CatalogItem objects to rank, or a tuple of (CatalogItem list, TagSpec)
        
    Returns:
        Ranked list of CatalogItem objects or RecommendOut if final recommendation
    """
    if isinstance(input_data, list):
        # Simple ranking of catalog items
        catalog_items = input_data
        
        # Score items based on type priority and randomization
        type_priorities = {
            "shirt": 10,
            "dress": 10,
            "pants": 9,
            "shorts": 9,
            "shoes": 8,
            "sneakers": 8,
            "boots": 8,
            "hat": 7,
            "cap": 7,
            "jacket": 6,
            "cape": 6,
            "tie": 5,
            "bow": 5,
            "accessory": 4,
            "necklace": 4,
            "bag": 3,
            "socks": 2,
            "hairpin": 1,
            "wristband": 1
        }
        
        # Score and sort items
        scored_items = []
        for item in catalog_items:
            base_score = type_priorities.get(item.type.lower(), 5)
            random_factor = random.uniform(0.8, 1.2)  # Add some randomization
            final_score = base_score * random_factor
            scored_items.append((final_score, item))
        
        # Sort by score (descending) and return items
        scored_items.sort(key=lambda x: x[0], reverse=True)
        return [item for score, item in scored_items]
    
    elif isinstance(input_data, tuple) and len(input_data) == 2:
        # Advanced ranking with TagSpec consideration
        catalog_items, tag_spec = input_data
        
        if not isinstance(catalog_items, list) or not all(isinstance(item, CatalogItem) for item in catalog_items):
            raise ValueError("First element of tuple must be a list of CatalogItem objects")
        
        if not isinstance(tag_spec, TagSpec):
            raise ValueError("Second element of tuple must be a TagSpec object")
        
        # Enhanced scoring based on TagSpec
        scored_items = []
        preferred_parts = tag_spec.parts or []
        theme = tag_spec.theme.lower()
        vibe = tag_spec.vibe or ""
        
        for item in catalog_items:
            base_score = 5.0  # Default score
            
            # Boost score if item type is in preferred parts
            if item.type.lower() in [part.lower() for part in preferred_parts]:
                base_score += 3.0
            
            # Theme-specific boosts
            if theme == "formal" and item.type.lower() in ["shirt", "pants", "tie", "jacket", "shoes"]:
                base_score += 2.0
            elif theme == "casual" and item.type.lower() in ["shirt", "pants", "hat", "shoes"]:
                base_score += 2.0
            elif theme == "sporty" and item.type.lower() in ["jersey", "shorts", "sneakers", "cap"]:
                base_score += 2.0
            elif theme == "gothic" and item.type.lower() in ["boots", "cape", "necklace"]:
                base_score += 2.0
            elif theme == "kawaii" and item.type.lower() in ["dress", "bow", "bag", "hairpin"]:
                base_score += 2.0
            
            # Vibe-specific adjustments
            if vibe == "dramatic" and item.type.lower() in ["cape", "boots", "necklace"]:
                base_score += 1.0
            elif vibe == "playful" and item.type.lower() in ["bow", "bag", "hairpin"]:
                base_score += 1.0
            elif vibe == "professional" and item.type.lower() in ["tie", "jacket"]:
                base_score += 1.0
            
            # Add randomization
            random_factor = random.uniform(0.9, 1.1)
            final_score = base_score * random_factor
            
            scored_items.append((final_score, item))
        
        # Sort by score and return items
        scored_items.sort(key=lambda x: x[0], reverse=True)
        ranked_items = [item for score, item in scored_items]
        
        return ranked_items
    
    else:
        raise ValueError(f"Unsupported input type: {type(input_data)}")