# Get input from the user
num1_str = input("Enter the first number: ")
num2_str = input("Enter the second number: ")

# Convert input strings to numbers (integers or floats)
# Use int() for whole numbers, float() for decimal numbers
try:
    num1 = float(num1_str)
    num2 = float(num2_str)

    # Perform addition
    sum_result = num1 + num2

    # Display the result
    print("The sum of", num1, "and", num2, "is:", sum_result)

except ValueError:
    print("Invalid input. Please enter valid numbers.")