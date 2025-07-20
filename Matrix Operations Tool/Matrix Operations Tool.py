import numpy as np

def input_matrix(name):
    rows = int(input(f"Enter number of rows for {name}: "))
    cols = int(input(f"Enter number of columns for {name}: "))
    print(f"Enter elements for {name} row-wise (space separated):")
    entries = list(map(float, input().split()))
    matrix = np.array(entries).reshape(rows, cols)
    return matrix

def display_menu():
    print("\nChoose the matrix operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Transpose")
    print("5. Determinant")
    print("6. Exit")

def main():
    while True:
        display_menu()
        choice = input("Enter option number: ")

        if choice in ['1', '2', '3']:
            a = input_matrix("Matrix A")
            b = input_matrix("Matrix B")
            if choice == '1':
                print("Result (A + B):\n", np.add(a, b))
            elif choice == '2':
                print("Result (A - B):\n", np.subtract(a, b))
            elif choice == '3':
                print("Result (A x B):\n", np.dot(a, b))
        elif choice == '4':
            a = input_matrix("Matrix")
            print("Transpose:\n", np.transpose(a))
        elif choice == '5':
            a = input_matrix("Matrix")
            if a.shape[0] == a.shape[1]:
                print("Determinant:", np.linalg.det(a))
            else:
                print("Determinant can only be found for square matrices.")
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
