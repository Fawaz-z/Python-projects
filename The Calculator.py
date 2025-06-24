operator = input("Enter a operator")
num1 = float(input("Enter a number"))
num2 = float(input("Enter another number"))

if operator == "+":
    num3 = num1 + num2
elif operator == "-":
    num3 = num1 - num2
elif operator == "*":
    num3 = num1 * num2
elif operator == "/":
    num3 = num1 / num2
else:
    print("operator means  either +, -, /, or, *")
print(str(num1) + ' + ' + str(num2) + ' = ' + str(num3))
