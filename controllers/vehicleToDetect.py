def toggle_classes(classes, classes_enabled, vehicle_types):
    try:
        for vehicle in vehicle_types:
            i = classes.index(vehicle)
            classes_enabled[i] = not classes_enabled[i]
            
        filtered_classes = [i for i in range(len(classes)) if classes_enabled[i]]
        return filtered_classes

    except ValueError as e:
        return f"Error: {e}. Vehicle type not found."

# Example usage
classes = ['car', 'motorcycle', 'jeepney', 'bus', 'tricycle', 'van', 'truck', 'taxi', 'modern_jeepney']
classes_enabled = [False] * 9
vehicle_types = ['car', 'taxi', 'jeepney']

result = toggle_classes(classes, classes_enabled, vehicle_types)
print(result)  # Expected output: [0, 2, 7]
