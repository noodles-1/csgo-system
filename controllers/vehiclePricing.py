import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

def updateVehiclePrice(vehicleType, newPrice, vehiclePrices):
    
    # Convert vehicleType to uppercase
    vehicleType = vehicleType.lower() # any input ni user will be all lowercase
    
    if vehicleType not in vehiclePrices:
        print("Error: Vehicle type not found.")
        return
    
    if not isinstance(newPrice, float):
        print("Error: Price should be a floating point number") # 0 - Infinity
        return
    
    if newPrice < 0:
        print("Error: Price should be non-negative.")
        return
    
    vehiclePrices[vehicleType] = newPrice # Simple assignment to the dictionary
    print(f"Price for {vehicleType} updated to {newPrice}.")

# Dictionary to store vehicle prices
vehiclePrices = {
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

# Example usage
updateVehiclePrice("car", 55.00, vehiclePrices)
