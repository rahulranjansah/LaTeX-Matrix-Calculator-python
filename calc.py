"""
Main
"""
from sympy import Matrix, latex, pprint

# create n numbers of n*n matrix
def create_matrix(matrix_count, rows, columns):
    """
    Forms n number of new matrix with "a" rows and "b" columns
    """
    matrix_list = []
    while matrix_count > 0:
        matrix = []
        try:
            for i in range(rows):
                row = []
                for j in range(columns):
                    entry = input(f"Row value at {(i+1)}{(j+1)} place: ")
                    row.append(entry)
                matrix.append(row)

            matrix = Matrix(matrix)
            matrix_list.append(matrix)

            matrix_count -= 1

            if matrix_count > 0:
                rows = int(input("No. of rows: "))
                columns  = int(input("No. of columns: "))

        except ValueError:
            print("Invalid Input re-entry of data required")

    return matrix_list

def validate_input():
    """
    Validate input reprompts for the input if you miss inputting values
    """
    while True:
        try:
            matrix_count = int(input("No. of unique matrix undergoing operations: "))
            if matrix_count > 0:
                return matrix_count
        except ValueError:
            print("ValueError: Invalid input. Please enter a positive number.")

def validate_rowcol():
    """
    Validates initializing the rows and columns of matrix
    No negative inputs of rows or column values
    """
    while True:
        try:
            row = int(input("No. of rows: "))
            col = int(input("No. of columns: "))
            if (row > 0) and (col > 0):
                return row, col

        except ValueError:
            print("Invalid Input re-enter positive value")

# sum and subtraction of matrix shape (m*n)
def add_subtract_matrix(matrix_list):
    """
    Sum/Subtracts n numbers a*b matrix with same dimensions together
    Additional feature for latex support
    """
    matrix_num = int(input("How many matrix participates in operation? "))
    latex_operation = []
    # first index defines what is the dimension of matrix after operation
    first_index = int(input("Left-most matrix index: "))
    first_matrix = matrix_list[first_index]

    latex_operation.append(first_matrix)
    # empty matrix initialize, print index on screen, and rows cols initialize
    operation_sum_sub = first_matrix

    for _ in range(matrix_num - 1):
        index = int(input("Index of matrix to the right: "))
        operation_type = input("What operation? Add[A] Subtract[S]:: ").upper().strip()

        # check dimensions of the matrix
        if (matrix_list[index].rows == first_matrix.rows
            and matrix_list[index].cols == first_matrix.cols):

            if operation_type == "A":
                operation_sum_sub += matrix_list[index]
                latex_operation.append("+")
                latex_operation.append(matrix_list[index])

            elif operation_type == "S":
                operation_sum_sub -= matrix_list[index]
                latex_operation.append("-")
                latex_operation.append(matrix_list[index])

            else:
                raise ValueError("Dimension out of range")

        else:
            raise ValueError("Error Row and Column input")
    print(latex_operation)
    return operation_sum_sub, latex_operation

# dot product matrix shape (m*n)
def dot_product_matrix(matrix_list):
    """
    Dot product of n numbers of a*b matrix with proper dimension
    Latex based output with intermediate steps and final solution
    """
    matrix_num = int(input("How many matrix participates in operation? "))

    # latex print of all matrix
    for matrix in matrix_list:
        with open("output.tex", "a", encoding="utf-8") as output_file:
            output_file.write("$"+ latex(matrix) + "$\n")

    with open("output.tex", "a", encoding="utf-8") as output_file:
        output_file.write(r"\\By law of commutativity, dot product of matrices right to left, \\")

    # first index defines what is the dimension of matrix after operation
    initialize_product = matrix_list[int(input("Which will be your Rightmost matrix: "))]

    # intermediate method print
    for _ in range(matrix_num-1):

        index = int(input("Inner matrix index: "))

        # intermediate steps
        steps = ["="]
        outer_product = initialize_product.T
        _, symbol_count = outer_product.shape
        outer_product =  outer_product.tolist()
        i = 0

        for element in outer_product:
            for atom, column in zip(element, range(matrix_list[index].cols)):
                step = str(latex(atom)) + str(latex(matrix_list[index].col(column)))
                steps.append(step)
                i += 1
                if i % symbol_count != 0:
                    steps.append("+")
                else:
                    steps.append("\\hspace{0.5cm}")
        print()

        # check dimensions of the matrix

        if matrix_list[index].cols == initialize_product.rows:
            initialize_product = matrix_list[index]*(initialize_product)
        else:
            print("Dimension out of range")

        for _ in steps:
            with open("output.tex", "a", encoding="utf-8") as output_file:
                output_file.write("\n$" + str(_) + "$")

    print(steps)

    return initialize_product

def operations():
    """
    Choose matrix summation or product
    """
    while True:
        operation_key = input("Operation key Product or Sum/Subtract [P/S]: ").upper().strip()

        if (operation_key in ["S", "P"]):
            return operation_key


def main():
    """
    Calling and Printing all the functions
    """
    # initialize new .txt file for LaTeX, future development targets user input to ask if "a" or "w"
    with open("output.txt", "w", encoding="utf-8") as output_file:
        output_file.write("")

    # validate user values
    validated_count = validate_input()
    validated_rows, validated_columns = validate_rowcol()

    matrix_list = create_matrix(validated_count, validated_rows, validated_columns)

    # enumerates on the screen to assist indexing
    for en_matrix in enumerate(matrix_list):
        pprint(en_matrix)

    operation_key = operations()

    if operation_key == "P":
        # intermediate steps
        product = dot_product_matrix(matrix_list)
        pprint(product)
        # latex_dot_product(matrix_list)
        with open("output.tex", "a", encoding="utf-8") as output_file:
            output_file.write("\n\n$="+ latex(product) + "$")

    elif operation_key == "S":
        sum_sub, latex_operation = add_subtract_matrix(matrix_list)
        pprint(sum_sub)
        for matrix in latex_operation:
            with open("output.tex", "a", encoding="utf-8") as output_file:
                output_file.write("$"+ latex(matrix) + "$")
        with open("output.txt", "a", encoding="utf-8") as output_file:
            output_file.write("\n\n$="+ latex(sum_sub) + "$")

    else:
        print("Error in input")

if __name__ == "__main__":
    main()
