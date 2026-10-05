while True:
    numero1 = float(input("Digite o primeiro número: "))
    operacao = input("Digite a operação (+, -, *, /, **): ")
    numero2 = float(input("Digite o segundo número: "))

    if operacao == "+":
        print(numero1 + numero2)

    elif operacao == "-":
        print(numero1 - numero2)

    elif operacao == "*":
        print(numero1 * numero2)

    elif operacao == "/":
        if numero2 == 0:
            print("Não é possível dividir por zero")
        else:
            print(numero1 / numero2)

    elif operacao == "**":
        print(numero1 ** numero2)

    else:
        print("Operação inválida")

    continuar = input("Deseja fazer outra operação? (s/n): ")

    if continuar == "n":
        break