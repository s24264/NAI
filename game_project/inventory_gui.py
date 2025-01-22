import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from equipment_system import Inventory, Item

class InventoryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Inventory")
        self.root.geometry("1200x900")  # Increased window size further
        
        # Create inventory instance
        self.inventory = Inventory(size=30)  # 5x6 grid
        self.image_cache = {}
        
        # Create main frames
        self.inventory_frame = ttk.Frame(root, padding="10")
        self.inventory_frame.grid(row=0, column=0, sticky="nsew")
        
        self.description_frame = ttk.Frame(root, padding="10")
        self.description_frame.grid(row=0, column=1, sticky="nsew")
        
        # Configure grid weights
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)
        
        self.create_inventory_grid()
        self.create_description_area()
        self.create_control_panel()
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure("Inventory.TFrame", padding=5)
        
        # Generate initial items
        self.setup_sample_items()
        
    def get_item_image(self, item, size=(64, 64)):
        """Get or generate an image for an item"""
        if not item:
            return None
            
        cache_key = f"{item.name}_{size[0]}x{size[1]}"
        if cache_key not in self.image_cache:
            img = self.inventory.get_item_visual(item, size)
            if img:
                self.image_cache[cache_key] = ImageTk.PhotoImage(img)
            else:
                return None
                
        return self.image_cache[cache_key]

    def setup_sample_items(self):
        """Add some sample items to the inventory"""
        # Generate random items of different types
        items = [
            # First row - weapons
            self.inventory.generate_random_item("sword"),
            self.inventory.generate_random_item("axe"),
            self.inventory.generate_random_item("bow"),
            self.inventory.generate_random_item("staff"),
            self.inventory.generate_random_item("wand"),
            self.inventory.generate_random_item("sword"),
            
            # Second row - defensive items
            self.inventory.generate_random_item("shield"),
            self.inventory.generate_random_item("shield"),
            self.inventory.generate_random_item("ring"),
            self.inventory.generate_random_item("amulet"),
            self.inventory.generate_random_item("ring"),
            self.inventory.generate_random_item("amulet"),
            
            # Third row - consumables
            self.inventory.generate_random_item("potion"),
            self.inventory.generate_random_item("scroll"),
            self.inventory.generate_random_item("potion"),
            self.inventory.generate_random_item("scroll"),
            self.inventory.generate_random_item("potion"),
            self.inventory.generate_random_item("scroll"),
            
            # Fourth row - mixed items
            self.inventory.generate_random_item("staff"),
            self.inventory.generate_random_item("wand"),
            self.inventory.generate_random_item("bow"),
            self.inventory.generate_random_item("axe"),
            self.inventory.generate_random_item("sword"),
            self.inventory.generate_random_item("shield")
        ]
        for item in items:
            self.inventory.add_item(item)
            
    def create_control_panel(self):
        """Create control panel for item generation"""
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        # Add item generation button
        generate_btn = ttk.Button(
            control_frame,
            text="Generate Random Item",
            command=self.generate_new_item
        )
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Add item type selection
        type_label = ttk.Label(control_frame, text="Item Type:")
        type_label.pack(side=tk.LEFT, padx=5)
        
        # Create dropdown menu with fixed values
        self.item_type_var = tk.StringVar(value="random")
        type_menu = ttk.OptionMenu(
            control_frame,
            self.item_type_var,
            "random",
            "random",
            *sorted(self.inventory.item_generator.item_types)
        )
        type_menu.pack(side=tk.LEFT, padx=5)
            
    def generate_new_item(self):
        """Generate and add a new random item"""
        item_type = None if self.item_type_var.get() == "random" else self.item_type_var.get()
        new_item = self.inventory.generate_random_item(item_type)
        if self.inventory.add_item(new_item):
            self.update_inventory_display()
        else:
            tk.messagebox.showwarning("Inventory Full", "No empty slots available!")
            
    def create_inventory_grid(self):
        """Create the grid of inventory slots"""
        self.slots = []
        for row in range(5):  # Changed to 5 rows
            for col in range(6):  # Changed to 6 columns
                slot_index = row * 6 + col  # Updated calculation
                
                # Create frame for each slot
                slot_frame = ttk.Frame(self.inventory_frame, style="Inventory.TFrame")
                slot_frame.grid(row=row, column=col, padx=5, pady=5)
                
                # Create canvas for item icon
                icon_canvas = tk.Canvas(slot_frame, width=40, height=40, bg="lightgray")
                icon_canvas.pack(pady=(5, 2))
                
                # Create label for item name
                name_label = ttk.Label(slot_frame, text="Empty")
                name_label.pack()
                
                # Bind click event to the whole slot
                icon_canvas.bind("<Button-1>", lambda e, idx=slot_index: self.show_item_details(idx))
                name_label.bind("<Button-1>", lambda e, idx=slot_index: self.show_item_details(idx))
                
                self.slots.append({
                    "frame": slot_frame,
                    "canvas": icon_canvas,
                    "label": name_label
                })
                
        self.update_inventory_display()
        
    def create_description_area(self):
        """Create the area for displaying item descriptions"""
        # Title label
        self.item_title = ttk.Label(
            self.description_frame,
            text="Select an item",
            font=("Arial", 14, "bold")
        )
        self.item_title.pack(pady=(0, 10))
        
        # Large item icon
        self.detail_canvas = tk.Canvas(
            self.description_frame,
            width=100,
            height=100,
            bg="lightgray"
        )
        self.detail_canvas.pack(pady=(0, 10))
        
        # Description text
        self.description_text = tk.Text(
            self.description_frame,
            wrap=tk.WORD,
            width=40,
            height=10,
            font=("Arial", 11)
        )
        self.description_text.pack(fill=tk.BOTH, expand=True)
        self.description_text.config(state=tk.DISABLED)
        
        # Attributes frame
        self.attributes_frame = ttk.LabelFrame(
            self.description_frame,
            text="Attributes",
            padding="5"
        )
        self.attributes_frame.pack(fill=tk.X, pady=(10, 0))
        
    def update_inventory_display(self):
        """Update the display of all inventory slots"""
        for i, slot in enumerate(self.slots):
            item = self.inventory.slots[i]
            if item:
                slot["label"].configure(text=item.name)
                img = self.get_item_image(item, (40, 40))
                if img:
                    slot["canvas"].delete("all")
                    slot["canvas"].create_image(20, 20, image=img, anchor="center")
            else:
                slot["label"].configure(text="Empty")
                slot["canvas"].delete("all")
                
    def show_item_details(self, slot_index):
        """Show details for the selected item"""
        self.inventory.select_slot(slot_index)
        item = self.inventory.slots[slot_index]
        
        # Update title and image
        if item:
            self.item_title.configure(text=str(item))
            img = self.get_item_image(item, (100, 100))
            if img:
                self.detail_canvas.delete("all")
                self.detail_canvas.create_image(50, 50, image=img, anchor="center")
                
            # Update attributes
            for widget in self.attributes_frame.winfo_children():
                widget.destroy()
                
            for attr, value in item.attributes.items():
                attr_label = ttk.Label(
                    self.attributes_frame,
                    text=f"{attr.title()}: {value}"
                )
                attr_label.pack(anchor="w")
        else:
            self.item_title.configure(text="Empty Slot")
            self.detail_canvas.delete("all")
            for widget in self.attributes_frame.winfo_children():
                widget.destroy()
            
        # Update description
        self.description_text.config(state=tk.NORMAL)
        self.description_text.delete(1.0, tk.END)
        
        if item:
            description = self.inventory.get_item_description()
            self.description_text.insert(tk.END, description)
        else:
            self.description_text.insert(tk.END, "No item in this slot.")
            
        self.description_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryGUI(root)
    root.mainloop() 