def main():
    vehicles = ["car", "motorcycle", "jeepney", "bus", "tricycle", "van", "truck", "taxi", "modern_jeepney"]

    while True:
        print("Choose a vehicle:")
        print("0: Car")
        print("1: Motorcycle")
        print("2: Jeepney")
        print("3: Bus")
        print("4: Tricycle")
        print("5: Van")
        print("6: Truck")
        print("7: Taxi")
        print("8: Modern Jeepney")
        print("9: Exit")

        choice = input("Enter the number of the vehicle: ")

        try:
            choice = int(choice)
            if 0 <= choice <= 8:
                print("You chose:", vehicles[choice])
            elif choice == 9:
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 0 and 8.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except IndexError:
            print("Invalid choice. Please enter a number between 0 and 8.")

if __name__ == "__main__":
    main()
