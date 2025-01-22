import random
from PIL import Image, ImageDraw

class ItemGeneratorAI:
    """First AI Model: Generates unique items with balanced attributes"""
    
    def __init__(self):
        self.name_prefixes = ["Ancient", "Mystic", "Divine", "Cursed", "Blessed", "Dragon", "Demon", "Angel"]
        self.name_suffixes = ["of Power", "of Wisdom", "of the Beast", "of Light", "of Darkness", "of Time"]
        self.item_types = ["sword", "shield", "potion", "staff", "scroll", "bow", "ring", "amulet", "axe", "wand"]
        self.rarities = ["common", "rare", "legendary"]
        self.attributes = {
            "sword": ["damage", "speed", "critical"],
            "shield": ["defense", "block", "reflection"],
            "potion": ["healing", "duration", "potency"],
            "staff": ["magic", "mana", "element"],
            "scroll": ["spell", "duration", "area"],
            "bow": ["range", "accuracy", "damage"],
            "ring": ["magic", "protection", "luck"],
            "amulet": ["magic", "wisdom", "resistance"],
            "axe": ["damage", "weight", "critical"],
            "wand": ["magic", "precision", "power"]
        }
        
        # Add attribute descriptions for all attributes
        self.attribute_templates = {
            "damage": "It deals {value} points of damage",
            "speed": "It strikes with {value} speed",
            "critical": "Has a {value}% chance of critical hit",
            "defense": "Provides {value} points of protection",
            "block": "Has {value}% chance to block",
            "reflection": "Reflects {value}% of damage",
            "healing": "Restores {value} health points",
            "duration": "Lasts for {value} turns",
            "potency": "Has {value} potency",
            "magic": "Channels {value} magical power",
            "mana": "Uses {value} mana points",
            "element": "Has {value} elemental power",
            "spell": "Contains level {value} spell",
            "area": "Affects {value} meter radius",
            "range": "Has {value} meter range",
            "accuracy": "Provides {value}% accuracy",
            "protection": "Grants {value} protection",
            "luck": "Increases luck by {value}",
            "wisdom": "Grants {value} wisdom",
            "resistance": "Provides {value} resistance",
            "weight": "Weighs {value} units",
            "precision": "Has {value}% precision",
            "power": "Contains {value} power"
        }
    
    def generate_item(self, item_type=None):
        """Generate a unique item with balanced stats"""
        if not item_type:
            item_type = random.choice(self.item_types)
            
        # Generate rarity with weights
        rarity = random.choices(self.rarities, weights=[60, 30, 10])[0]
        
        # Generate name
        prefix = random.choice(self.name_prefixes)
        base_name = item_type.title()
        suffix = random.choice(self.name_suffixes) if random.random() < 0.5 else ""
        name = f"{prefix} {base_name} {suffix}".strip()
        
        # Generate attributes based on rarity
        attributes = {}
        if item_type in self.attributes:
            for attr in self.attributes[item_type]:
                base_value = random.randint(1, 10)
                rarity_multiplier = 1 if rarity == "common" else 1.5 if rarity == "rare" else 2
                attributes[attr] = round(base_value * rarity_multiplier)
        
        return {
            "name": name,
            "type": item_type,
            "rarity": rarity,
            "attributes": attributes
        }

class DescriptionGeneratorAI:
    """Second AI Model: Generates dynamic item descriptions"""
    
    def __init__(self):
        self.templates = {
            "legendary": [
                "A legendary {type} of immense power. {attribute_desc} This artifact has been wielded by ancient heroes and kings.",
                "An extraordinary {type} that radiates pure energy. {attribute_desc} Legends say it was forged by the gods themselves."
            ],
            "rare": [
                "A remarkable {type} of exceptional quality. {attribute_desc} Such items are highly sought after by collectors.",
                "An impressive {type} with unique properties. {attribute_desc} Its craftsmanship is truly remarkable."
            ],
            "common": [
                "A reliable {type} of good make. {attribute_desc} It serves its purpose well.",
                "A solid {type} of standard quality. {attribute_desc} A trustworthy companion in any adventure."
            ]
        }
        
        self.attribute_templates = {
            "damage": "It deals {value} points of damage",
            "speed": "It strikes with {value} speed",
            "defense": "It provides {value} points of protection",
            "healing": "It restores {value} health points",
            "magic": "It channels {value} magical power"
        }
    
    def generate_description(self, item_data):
        """Generate a detailed description based on item properties"""
        # Select template based on rarity
        template = random.choice(self.templates[item_data["rarity"]])
        
        # Generate attribute description
        attribute_desc = []
        for attr, value in item_data["attributes"].items():
            if attr in self.attribute_templates:
                desc = self.attribute_templates[attr].format(value=value)
                attribute_desc.append(desc)
        
        attribute_text = ". ".join(attribute_desc) + "." if attribute_desc else ""
        
        # Format final description
        return template.format(
            type=item_data["type"],
            attribute_desc=attribute_text
        )

class VisualGeneratorAI:
    """Third AI Model: Generates item visuals"""
    
    def __init__(self):
        self.colors = {
            "legendary": "#FFD700",  # Gold
            "rare": "#C0C0C0",      # Silver
            "common": "#CD853F"      # Brown
        }
        self.glow_colors = {
            "legendary": "#FFF7D6",  # Light gold
            "rare": "#E8E8E8",       # Light silver
            "common": "#E6C5A5"      # Light brown
        }
    
    def generate_visual(self, item_data, size=(64, 64)):
        """Generate a visual representation of the item"""
        img = Image.new('RGBA', size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        color = self.colors.get(item_data["rarity"], "#808080")
        glow = self.glow_colors.get(item_data["rarity"], "#A8A8A8")
        
        width, height = size
        center_x = width // 2
        center_y = height // 2
        
        # Add rarity glow effect
        if item_data["rarity"] == "legendary":
            for i in range(3):
                draw.ellipse([0+i*2, 0+i*2, width-i*2, height-i*2], 
                           outline=self.glow_colors["legendary"])
        elif item_data["rarity"] == "rare":
            draw.ellipse([2, 2, width-2, height-2], 
                        outline=self.glow_colors["rare"])
        
        # Draw item based on type
        if item_data["type"] == "sword":
            # Blade glow and blade
            draw.line([(center_x, 8), (center_x, height-8)], fill=glow, width=5)
            draw.line([(center_x, 5), (center_x, height-5)], fill=color, width=3)
            # Guard
            draw.rectangle([center_x-15, center_y-3, center_x+15, center_y+3], fill=color)
            # Handle
            draw.rectangle([center_x-2, center_y+3, center_x+2, height-10], fill=color)
            # Pommel
            draw.ellipse([center_x-4, height-12, center_x+4, height-4], fill=color)
            
        elif item_data["type"] == "shield":
            # Shield glow and main shield
            draw.arc([5, 5, width-5, height-5], 0, 180, fill=glow, width=4)
            draw.arc([8, 8, width-8, height-8], 0, 180, fill=color, width=2)
            # Shield design
            draw.line([(8, center_y), (width-8, center_y)], fill=color, width=2)
            draw.line([(center_x, 10), (center_x, center_y+5)], fill=color, width=2)
            
        elif item_data["type"] == "potion":
            # Bottle glow
            draw.ellipse([center_x-12, height-35, center_x+12, height-11], fill=glow)
            # Bottle
            points = [(center_x-8, height//2), (center_x-12, height-15),
                     (center_x+12, height-15), (center_x+8, height//2)]
            draw.polygon(points, fill=color)
            # Neck and cork
            draw.rectangle([center_x-5, height//2-12, center_x+5, height//2], fill=color)
            draw.rectangle([center_x-4, height//2-18, center_x+4, height//2-12], fill="#8B4513")
            
        elif item_data["type"] == "staff":
            # Staff glow and pole
            draw.line([(center_x, 8), (center_x, height-8)], fill=glow, width=5)
            draw.line([(center_x, 5), (center_x, height-5)], fill=color, width=3)
            # Orb with glow
            draw.ellipse([center_x-12, 3, center_x+12, 27], fill=glow)
            draw.ellipse([center_x-10, 5, center_x+10, 25], fill=color)
            
        elif item_data["type"] == "scroll":
            # Scroll glow and main part
            draw.rectangle([12, center_y-17, width-12, center_y+17], fill=glow)
            draw.rectangle([15, center_y-15, width-15, center_y+15], fill=color)
            # Scroll ends
            draw.ellipse([8, center_y-15, 22, center_y+15], fill=color)
            draw.ellipse([width-22, center_y-15, width-8, center_y+15], fill=color)
            
        elif item_data["type"] == "bow":
            # Bow glow and main bow
            draw.arc([5, 5, width-5, height-5], -35, 35, fill=glow, width=4)
            draw.arc([8, 8, width-8, height-8], -30, 30, fill=color, width=3)
            # String and handle
            draw.line([(12, center_y), (width-12, center_y)], fill=color, width=2)
            for i in range(-5, 6, 5):
                draw.line([(center_x-5, center_y+i), (center_x+5, center_y+i)], fill=color, width=1)
            
        elif item_data["type"] == "ring":
            # Ring glow and main ring
            padding = width // 4
            draw.ellipse([padding-2, padding-2, width-padding+2, height-padding+2], fill=glow)
            draw.ellipse([padding, padding, width-padding, height-padding], outline=color, width=3)
            # Gem for legendary/rare
            if item_data["rarity"] in ["legendary", "rare"]:
                draw.ellipse([center_x-4, padding-2, center_x+4, padding+6], 
                           fill="#FF0000" if item_data["rarity"] == "legendary" else "#0000FF")
            
        elif item_data["type"] == "amulet":
            # Chain glow and chain
            draw.line([(center_x, 12), (center_x, height-15)], fill=glow, width=4)
            draw.line([(center_x, 10), (center_x, height-15)], fill=color, width=2)
            # Pendant with glow
            draw.ellipse([center_x-17, height-32, center_x+17, height-3], fill=glow)
            draw.ellipse([center_x-15, height-30, center_x+15, height-5], fill=color)
            
        elif item_data["type"] == "axe":
            # Handle glow and handle
            draw.line([(center_x, 8), (center_x, height-8)], fill=glow, width=4)
            draw.line([(center_x, 5), (center_x, height-5)], fill=color, width=2)
            # Blade with glow
            blade_points = [(center_x, 15), (center_x-15, 5), 
                          (center_x-15, 25), (center_x, 35)]
            draw.polygon([(p[0]-2, p[1]-2) for p in blade_points], fill=glow)
            draw.polygon(blade_points, fill=color)
            
        elif item_data["type"] == "wand":
            # Wand glow and main wand
            draw.line([(18, height-13), (width-18, 13)], fill=glow, width=4)
            draw.line([(15, height-10), (width-15, 10)], fill=color, width=2)
            # Tip with glow
            draw.ellipse([width-27, 3, width-13, 17], fill=glow)
            draw.ellipse([width-25, 5, width-15, 15], fill=color)
            
        return img 