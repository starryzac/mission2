def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "错误：除数不能为零"
    return a / b


if __name__ == "__main__":
    print("===== 简易计算器 =====")
    print("支持运算: +  -  *  /")
    print("输入 'q' 退出")

    while True:
        expr = input("\n请输入算式 (如 1 + 2): ").strip()
        if expr.lower() == 'q':
            print("再见！")
            break

        parts = expr.split()
        if len(parts) != 3:
            print("格式错误，请输入: 数字 运算符 数字")
            continue

        try:
            a = float(parts[0])
            b = float(parts[2])
        except ValueError:
            print("请输入有效的数字")
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
            print(f"不支持的运算符: {op}")
            continue

        print(f"结果: {result}")

