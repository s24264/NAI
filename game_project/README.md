# Game Inventory System

A Python-based inventory system for games with procedurally generated items, descriptions, and visuals.

## Features

- Procedurally generated items with unique attributes
- Dynamic item descriptions based on item properties
- Visual representation of items with rarity effects
- 30-slot inventory system with drag-and-drop interface
- Item generation with different rarities (common, rare, legendary)

## Project Structure

```
game_project/
├── requirements.txt        # Project dependencies
├── README.md              # This file
├── ai_models.py           # AI models for item generation
├── equipment_system.py    # Core inventory system
└── inventory_gui.py       # Graphical user interface
```

## Installation

1. Make sure you have Python 3.7 or higher installed
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Run the following command from the project directory:
```bash
python inventory_gui.py
```

## Usage

- Click "Generate Random Item" to create new items
- Use the dropdown to select specific item types
- Click on items to view their details
- Items are automatically colored based on rarity:
  - Legendary: Gold
  - Rare: Silver
  - Common: Brown

## Models

The system uses three AI models:
1. ItemGeneratorAI: Generates balanced items with attributes
2. DescriptionGeneratorAI: Creates dynamic item descriptions
3. VisualGeneratorAI: Generates visual representations of items 