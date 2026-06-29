def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "Error: division by zero"
    return a / b


if __name__ == "__main__":
    print("===== Simple Calculator =====")
    print("Operations: +  -  *  /")
    print("Enter 'q' to quit")

    while True:
        expr = input("\nEnter expression (e.g. 1 + 2): ").strip()
        if expr.lower() == 'q':
            print("Goodbye!")
            break

        parts = expr.split()
        if len(parts) != 3:
            print("Invalid format, use: number operator number")
            continue

        try:
            a = float(parts[0])
            b = float(parts[2])
        except ValueError:
            print("Please enter valid numbers")
            continue

        op = parts[1]
        if op == '+':
            result = add(a, b)
        elif op == '-':
            result = subtract(a, b)
        elif op == '*':
            result = multiply(a, b)
        elif op == '/':
            result = divide(a, b)
        else:
            print(f"Unsupported operator: {op}")
            continue

        print(f"Result: {result}")

