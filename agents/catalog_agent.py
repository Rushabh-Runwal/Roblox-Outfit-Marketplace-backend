"""
Catalog agent for fetching and managing outfit items from the Roblox catalog.
This agent handles communication with external APIs and catalog data management.
"""

from typing import List, Union
import random
from .contracts import TagSpec, CatalogItem, RecommendIn


def run(input_data: Union[TagSpec, RecommendIn]) -> List[CatalogItem]:
    """
    Run the catalog agent with the given input.
    
    Args:
        input_data: Either TagSpec or RecommendIn contract
        
    Returns:
        List of CatalogItem objects matching the specifications
    """
    if isinstance(input_data, TagSpec):
        # Handle TagSpec input for detailed catalog search
        theme = input_data.theme.lower()
        parts = input_data.parts or ["shirt", "pants", "shoes", "accessories"]
        
        # Generate catalog items based on theme and parts specification
        catalog_items = []
        
        # Sample asset ID base numbers for different themes
        theme_bases = {
            "formal": 7890000000,
            "casual": 1234000000,
            "sporty": 1356000000,
            "gothic": 1912000000,
            "kawaii": 2578000000
        }
        
        base_id = theme_bases.get(theme, 1000000000)
        
        for i, part in enumerate(parts[:6]):  # Limit to 6 items
            asset_id = str(base_id + i * 111111)
            catalog_items.append(CatalogItem(assetId=asset_id, type=part))
        
        return catalog_items
    
    elif isinstance(input_data, RecommendIn):
        # Handle RecommendIn input for basic theme-based search
        theme = input_data.theme.lower()
        
        # Sample catalog data for different themes
        sample_catalogs = {
            "formal": [
                CatalogItem(assetId="7890123456", type="shirt"),
                CatalogItem(assetId="8901234567", type="pants"),
                CatalogItem(assetId="9012345678", type="tie"),
                CatalogItem(assetId="1023456789", type="shoes"),
                CatalogItem(assetId="1134567890", type="jacket")
            ],
            "casual": [
                CatalogItem(assetId="1234567890", type="shirt"),
                CatalogItem(assetId="2345678901", type="pants"),
                CatalogItem(assetId="3456789012", type="hat"),
                CatalogItem(assetId="4567890123", type="shoes"),
                CatalogItem(assetId="5678901234", type="accessory")
            ],
            "sporty": [
                CatalogItem(assetId="1356789012", type="jersey"),
                CatalogItem(assetId="1467890123", type="shorts"),
                CatalogItem(assetId="1578901234", type="sneakers"),
                CatalogItem(assetId="1689012345", type="cap"),
                CatalogItem(assetId="1790123456", type="socks")
            ],
            "gothic": [
                CatalogItem(assetId="1912345678", type="shirt"),
                CatalogItem(assetId="2023456789", type="pants"),
                CatalogItem(assetId="2134567890", type="boots"),
                CatalogItem(assetId="2245678901", type="cape"),
                CatalogItem(assetId="2356789012", type="necklace")
            ],
            "kawaii": [
                CatalogItem(assetId="2578901234", type="dress"),
                CatalogItem(assetId="2689012345", type="bow"),
                CatalogItem(assetId="2790123456", type="shoes"),
                CatalogItem(assetId="2801234567", type="bag"),
                CatalogItem(assetId="2912345678", type="hairpin")
            ]
        }
        
        # Get catalog items for the theme, or use casual as default
        catalog_items = sample_catalogs.get(theme, sample_catalogs["casual"])
        
        # Randomize and return 6-10 items (or all available if fewer than 6)
        random.shuffle(catalog_items)
        max_items = min(10, len(catalog_items))
        min_items = min(6, len(catalog_items))
        num_items = random.randint(min_items, max_items) if max_items > min_items else max_items
        return catalog_items[:num_items]
    
    else:
        raise ValueError(f"Unsupported input type: {type(input_data)}")