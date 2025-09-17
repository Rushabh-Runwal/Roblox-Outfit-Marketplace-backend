"""
Orchestrator agent for coordinating other agents in the outfit recommendation system.
The orchestrator manages the flow between different agents to provide comprehensive recommendations.
"""

from typing import Union
from .contracts import ChatIn, ChatOut, RecommendIn, RecommendOut


def run(input_data: Union[ChatIn, RecommendIn]) -> Union[ChatOut, RecommendOut]:
    """
    Run the orchestrator agent with the given input.
    
    Args:
        input_data: Either ChatIn or RecommendIn contract
        
    Returns:
        Either ChatOut or RecommendOut contract based on input type
    """
    if isinstance(input_data, ChatIn):
        # Handle chat orchestration
        return ChatOut(
            success=True,
            user_id=input_data.user_id,
            reply="Orchestrator: Processing your request through our AI style system!"
        )
    elif isinstance(input_data, RecommendIn):
        # Handle recommendation orchestration
        from .contracts import CatalogItem
        
        # Create sample outfit items for demonstration
        sample_outfit = [
            CatalogItem(assetId="1234567890", type="shirt"),
            CatalogItem(assetId="2345678901", type="pants"),
            CatalogItem(assetId="3456789012", type="shoes")
        ]
        
        return RecommendOut(
            success=True,
            user_id=input_data.user_id,
            message=f"Orchestrator: Your {input_data.theme} outfit has been coordinated!",
            outfit=sample_outfit
        )
    else:
        raise ValueError(f"Unsupported input type: {type(input_data)}")