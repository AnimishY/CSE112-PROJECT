

# Example usage
X = 10
Y = 20

variable_to_modify = input("Enter the variable to modify (X or Y): ")
new_value = int(input("Enter the new value: "))

globals()[variable_to_modify] = globals()[variable_to_modify] + globals()[variable_to_modify]

print(f"X: {X}, Y: {Y}")