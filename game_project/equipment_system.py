from ai_models import ItemGeneratorAI, DescriptionGeneratorAI, VisualGeneratorAI
from typing import List, Dict, Optional

class Item:
    def __init__(self, name: str, item_type: str, rarity: str, attributes: Dict = None):
        self.name = name
        self.item_type = item_type
        self.rarity = rarity
        self.attributes = attributes or {}
        
    def __str__(self):
        return f"{self.name} ({self.rarity} {self.item_type})"

class Inventory:
    def __init__(self, size: int = 10):
        self.size = size
        self.slots: List[Optional[Item]] = [None] * size
        self.selected_slot: Optional[int] = None
        
        # Initialize AI models
        self.item_generator = ItemGeneratorAI()
        self.description_generator = DescriptionGeneratorAI()
        self.visual_generator = VisualGeneratorAI()
    
    def add_item(self, item: Item) -> bool:
        """Add an item to the first empty slot."""
        for i in range(self.size):
            if self.slots[i] is None:
                self.slots[i] = item
                return True
        return False
    
    def select_slot(self, slot_index: int) -> bool:
        """Select a slot to view item details."""
        if 0 <= slot_index < self.size:
            self.selected_slot = slot_index
            return True
        return False
    
    def get_item_description(self) -> str:
        """Get AI-generated description of the currently selected item."""
        if self.selected_slot is None or self.slots[self.selected_slot] is None:
            return "No item selected."
        
        item = self.slots[self.selected_slot]
        item_data = {
            "name": item.name,
            "type": item.item_type,
            "rarity": item.rarity,
            "attributes": item.attributes
        }
        return self.description_generator.generate_description(item_data)
    
    def generate_random_item(self, item_type: str = None) -> Item:
        """Generate a random item using the Item Generator AI."""
        item_data = self.item_generator.generate_item(item_type)
        return Item(
            item_data["name"],
            item_data["type"],
            item_data["rarity"],
            item_data["attributes"]
        )
    
    def get_item_visual(self, item: Item, size=(64, 64)):
        """Get AI-generated visual for an item."""
        if not item:
            return None
            
        item_data = {
            "name": item.name,
            "type": item.item_type,
            "rarity": item.rarity,
            "attributes": item.attributes
        }
        return self.visual_generator.generate_visual(item_data, size)

# Example usage
if __name__ == "__main__":
    # Create inventory
    inventory = Inventory(size=5)
    
    # Create some sample items
    sword = Item("Excalibur", "sword", "legendary")
    shield = Item("Dragon Shield", "shield", "rare")
    
    # Add items to inventory
    inventory.add_item(sword)
    inventory.add_item(shield)
    
    # Select and get description of an item
    inventory.select_slot(0)  # Select first slot
    print(inventory.get_item_description())
