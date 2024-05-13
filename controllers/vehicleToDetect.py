classes = ['car', 'motorcycle', 'jeepney', 'bus', 'tricycle', 'van', 'truck', 'taxi', 'modern_jeepney']
classes_enabled = [False] * 9

try:
    i = classes.index('car')
    classes_enabled[i] = not classes_enabled[i]

    i = classes.index('taxi')
    classes_enabled[i] = not classes_enabled[i]

    i = classes.index('jeepney')
    classes_enabled[i] = not classes_enabled[i]

    filtered_classes = [i for i in range(len(classes)) if classes_enabled[i]]
    print(filtered_classes)

except ValueError as e:
    print(f"Error: {e}. Vehicle type not found.")
