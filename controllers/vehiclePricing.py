import tkinter as tk
from tkinter import ttk


class VehiclePricingApp:
    def __init__(self, vehicle_prices):
        self.vehicle_prices = vehicle_prices
        self.entry_vars = {}  # Dictionary to store StringVar objects

        self.root = tk.Tk()
        self.root.title("Vehicle Pricing")

        self.create_vehicle_entries()

        update_button = ttk.Button(self.root, text="Update Prices", command=self.update_prices)
        update_button.pack(pady=10)

        self.root.mainloop()

    def create_vehicle_entries(self):
        for vehicle, price in self.vehicle_prices.items():
            frame = ttk.Frame(self.root)
            frame.pack(pady=5)

            label = ttk.Label(frame, text=f"{vehicle.capitalize()} Price:")
            label.grid(row=0, column=0)

            entry_var = tk.StringVar()
            entry_var.set(f"{price:.2f}")
            entry = ttk.Entry(frame, textvariable=entry_var)
            entry.grid(row=0, column=1)

            self.entry_vars[vehicle] = entry_var

    def update_prices(self):
        for vehicle, entry_var in self.entry_vars.items():
            try:
                new_price = float(entry_var.get())
                self.vehicle_prices[vehicle] = new_price
                entry_var.set(f"{new_price:.2f}")  # Update displayed price
            except ValueError:
                pass


# Dictionary to store vehicle prices
vehicle_prices = {
    "car": 50.00,
    "motorcycle": 30.00,
    "jeepney": 50.00,
    "bus": 70.00,
    "tricycle": 20.00,
    "van": 80.00,
    "truck": 100.00,
    "taxi": 50.00,
    "modern_jeepney": 40.00
}

# Run the application
if __name__ == "__main__":
    app = VehiclePricingApp(vehicle_prices)
