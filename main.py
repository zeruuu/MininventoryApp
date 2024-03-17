import tkinter as tk # For the GUI
from tkinter import ttk # For the Treeview
from tkinter import filedialog # For file management

class EditItemWindow(tk.Toplevel): # Edit Item Window
    def __init__(self, parent, item_values, edit_item_callback):
        super().__init__(parent)
        self.parent = parent
        self.title("Edit Item")
        self.geometry('300x150')

        # Labels
        tk.Label(self, text="Item Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(self, text="Price:").grid(row=2, column=0, padx=5, pady=5)

        # Entry widgets
        self.item_name_entry = tk.Entry(self)
        self.item_name_entry.insert(tk.END, item_values[0])
        self.item_name_entry.grid(row=0, column=1, columnspan=2, padx=15, pady=5)

        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.insert(tk.END, item_values[1])
        self.quantity_entry.grid(row=1, column=1, columnspan=2, padx=15, pady=5)
        self.quantity_entry.config(validate="key", validatecommand=(self.register(self.validate_quantity), "%P"))

        self.price_entry = tk.Entry(self)
        self.price_entry.insert(tk.END, item_values[2])
        self.price_entry.grid(row=2, column=1, columnspan=2, padx=15, pady=5)
        self.price_entry.config(validate="key", validatecommand=(self.register(self.validate_price), "%P"))

        # Edit button
        tk.Button(self, text="Edit", command=edit_item_callback).grid(row=3, column=0, columnspan=2, pady=10)

    def validate_quantity(self, new_value):
        return new_value.isdigit() or new_value == ""

    def validate_price(self, new_value):
        try:
            float(new_value)
            return True
        except ValueError:
            return False

class AddItemWindow(tk.Toplevel): # Add Item Window
    def __init__(self, parent, add_item_callback):
        super().__init__(parent)
        self.parent = parent
        self.title("Add Item")
        self.geometry('300x150')

        # Labels
        tk.Label(self, text="Item Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(self, text="Price:").grid(row=2, column=0, padx=5, pady=5)

        # Entry widgets
        self.item_name_entry = tk.Entry(self)
        self.item_name_entry.grid(row=0, column=1, columnspan=2, padx=15, pady=5)

        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.grid(row=1, column=1, columnspan=2, padx=15, pady=5)
        self.quantity_entry.config(validate="key", validatecommand=(self.register(self.validate_quantity), "%P"))

        self.price_entry = tk.Entry(self)
        self.price_entry.grid(row=2, column=1, columnspan=2, padx=15, pady=5)
        self.price_entry.config(validate="key", validatecommand=(self.register(self.validate_price), "%P"))

        # Add button
        tk.Button(self, text="Add", command=add_item_callback).grid(row=3, column=0, columnspan=2, pady=10)

    # Validates whether the input for Quantity and Price is numeric.
    def validate_quantity(self, new_value):
        return new_value.isdigit() or new_value == ""

    def validate_price(self, new_value):
        try:
            float(new_value)
            return True
        except ValueError:
            return False

class InventorySystem: # Main Program
    def __init__(self, root):
        self.root = root
        self.root.title("Mininventory Manager")
        self.inventory = [] # Inventory List
        self.add_window = None
        self.create_gui()

    # Main Program GUI
    def create_gui(self):
        # Buttons
        tk.Button(self.root, text="Add Item", command=self.open_add_window).grid(row=3, column=0, pady=5)
        tk.Button(self.root, text="Edit Item", command=self.edit_item_window).grid(row=3, column=1, pady=5)
        tk.Button(self.root, text="Delete Item", command=self.delete_item).grid(row=3, column=2, pady=5)
        tk.Button(self.root, text="Open File", command=self.open_file).grid(row=2, column=0, pady=5)
        tk.Button(self.root, text="Save File", command=self.save_file).grid(row=2, column=1, pady=5)
        tk.Button(self.root, text="Sort by Name", command=lambda: self.sort_inventory("name")).grid(row=4, column=0, pady=5)
        tk.Button(self.root, text="Sort by Quantity", command=lambda: self.sort_inventory("quantity")).grid(row=4, column=1, pady=5)
        tk.Button(self.root, text="Sort by Price", command=lambda: self.sort_inventory("price")).grid(row=4, column=2, pady=5)

        # Treeview for displaying the inventory
        self.tree = ttk.Treeview(self.root, columns=("Name", "Quantity", "Price"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.grid(row=5, column=0, columnspan=4, padx=5, pady=5)

    def edit_item_window(self):  # Function for Opening 'Edit Item' Window
        selected_item = self.tree.selection()[0]
        item_values = self.tree.item(selected_item, 'values')
        self.edit_window = EditItemWindow(self.root, item_values, self.edit_item)

    def edit_item(self):
        # Get the selected item from the Treeview
        selected_item = self.tree.selection()[0]

        # Get the item's values
        item_values = self.tree.item(selected_item, 'values')

        # Get edited values
        new_name = self.edit_window.item_name_entry.get()
        new_quantity = self.edit_window.quantity_entry.get()
        new_price = self.edit_window.price_entry.get()

        # Convert item_values to tuple if it's a string
        if isinstance(item_values, str):
            item_values = tuple(item_values.split())

        # Update the values in the Treeview
        self.tree.item(selected_item, values=(new_name, new_quantity, new_price))

        # Update the selected item's values in the inventory list
        for item in self.inventory:
            if item[:3] == item_values:
                # Convert the tuple to a list
                item_list = list(item)
                # Update the values
                item_list[0] = new_name
                item_list[1] = new_quantity
                item_list[2] = new_price
                # Convert the list back to a tuple
                updated_item = tuple(item_list)
                # Update the item in the inventory list
                index = self.inventory.index(item)
                self.inventory[index] = updated_item
                break

        # Sort the inventory list after editing
        self.sort_inventory("name")  # Sort by name by default

        # Close the edit window
        self.edit_window.destroy()

    def open_add_window(self): # Function for Opening 'Add Item' Window
        self.add_window = AddItemWindow(self.root, self.add_item)

    def open_file(self): # Open a saved file from a directory.
        for item in self.tree.get_children():
            self.inventory.clear()
            self.tree.delete(item)

        filename = filedialog.askopenfilename(initialdir='C:test', title='Open Inventory File')
        if filename:
            with open(filename, 'r') as file:
                for line in file:
                    # Parse each line into a tuple and append to the inventory
                    item = tuple(line.strip().split())
                    self.inventory.append(item)

            self.refresh_treeview()

    def save_file(self): # Save the current items into a file.
        filename = filedialog.asksaveasfilename(initialdir="C:/inventory_demo", title="Save File")
        if filename:
            with open(filename, 'w') as inventoryfile:
                for item in self.inventory:
                    # Convert tuple to string before writing
                    item_str = ' '.join(item) if isinstance(item, tuple) else item
                    inventoryfile.write(item_str + '\n')
    def add_item(self):
        item_name = self.add_window.item_name_entry.get()
        quantity = self.add_window.quantity_entry.get()
        price = self.add_window.price_entry.get()

        if item_name and quantity and price:
            item = (item_name, quantity, price)
            self.inventory.append(item)

            self.tree.insert("", "end", values=item)

            # Delete the inputs in the entry grids
            self.add_window.item_name_entry.delete(0, tk.END)
            self.add_window.quantity_entry.delete(0, tk.END)
            self.add_window.price_entry.delete(0, tk.END)

    def delete_item(self):
        # Get the selected item from the Treeview
        selected_item = self.tree.selection()[0]

        # Get the item's values
        item_values = self.tree.item(selected_item, 'values')

        # Iterate over the inventory list to find the item and delete it
        for index, item in enumerate(self.inventory):
            if item[:3] == item_values:
                del self.inventory[index]
                break

        # Delete the item from the Treeview
        self.tree.delete(selected_item)


    # Sort the Treeview items based on key value 'name' / 'quantity' / 'price'
    def sort_inventory(self, key):
        self.inventory.sort(key=lambda x: x[self.get_sort_index(key)])
        self.refresh_treeview()

    # Refreshes the Treeview when sorting
    def refresh_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for item in self.inventory:
            self.tree.insert("", "end", values=item)

    # Different sorting buttons have their own key values
    def get_sort_index(self, key):
        if key == "name":
            return 0
        elif key == "quantity":
            return 1
        elif key == "price":
            return 2
        else:
            return 0

if __name__ == "__main__":
    root = tk.Tk()
    app = InventorySystem(root)
    icon = tk.PhotoImage(file='inventoryico.png')
    root.iconphoto(True, icon)
    root.mainloop()