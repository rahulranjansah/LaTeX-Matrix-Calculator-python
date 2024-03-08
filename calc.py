from sympy import *

# create n numbers of n*n matrix
def create_matrix(matrix_count, rows, columns):

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
    while True:
        try:  
            matrix_count = int(input("No. of unique matrix undergoing operations: "))
            if matrix_count > 0:
                return matrix_count
            else:
                print("ValueError: Invalid input. Please enter a positive number.")
        except ValueError:
            print("ValueError: Invalid input. Please enter a positive number.")

def validate_rowcol():
    while True:
        try:
            row = int(input("No. of rows: "))
            col = int(input("No. of columns: "))
            if (row > 0) and (col > 0):
                return row, col
            elif (row < 0) or (col < 0):
                row = int(input("No. of rows: "))
                col = int(input("No. of columns: "))

        except ValueError:
            print("Invalid Input re-enter positive value")

# sum and subtraction of matrix shape (m*n)
def add_subtract_matrix(matrix_list):

    matrix_num = int(input("How many matrix participates in operation? "))
    latex_operation = []
    # first index defines what is the dimension of matrix after operation, dimensions stays same through out
    first_index = int(input("Left-most matrix index: "))
    first_matrix = matrix_list[first_index]

    latex_operation.append(first_matrix)
    # empty matrix initialize, print index on screen, and rows cols initialize
    operation_sum_sub = first_matrix

    for _ in range(matrix_num - 1): 

        index = int(input("Index of matrix to the right: "))

        operation_type = input("What operation do you want to do? Add - press A or a, Subtract - press S or s:: ")

        # check dimensions of the matrix
        if (matrix_list[index].rows == first_matrix.rows) and (matrix_list[index].cols == first_matrix.cols):

            if operation_type == "A" or operation_type == "a":
                operation_sum_sub += matrix_list[index]
                latex_operation.append("+")
                latex_operation.append(matrix_list[index])

            elif operation_type == "S" or operation_type == "s":
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
    matrix_num = int(input("How many matrix participates in operation? "))
    
    # latex print of all matrix
    for matrix in matrix_list:
        with open("output.txt", "a") as f:
            f.write("$"+ latex(matrix) + "$")

    # first index defines what is the dimension of matrix after operation, dimensions stays same through out
    first_matrix = matrix_list[int(input("Which will be your Rightmost matrix: "))]

    # initialize rightmost matrix 
    initialize_product = first_matrix

    for _ in range(matrix_num-1):

        index = int(input("Inner matrix index: "))

        # check dimensions of the matrix

        if (matrix_list[index].cols == initialize_product.rows):
            initialize_product = matrix_list[index]*(initialize_product)
        else:
            print("Dimension out of range")

    return initialize_product
         
def operations():
    while True: 
        operation_key = input("Operation key Product -> P and Sum/Subtract -> S: ")

        if (operation_key == "S") or (operation_key == "P"):
            return operation_key
        else:
            operation_key = input("Operation key Product -> P and Sum/Subtract -> S: ")
    
def main():
    # initialize new .txt file to be copied in LaTeX, future development targets user input to ask if "a" or "w"
    with open("output.txt", "w") as f:
        f.write("")

    # validate user values
    validated_count = validate_input()
    validated_rows, validated_columns = validate_rowcol() 

    matrix_list = create_matrix(validated_count, validated_rows, validated_columns)

    # enumerates on the screen to assist indexing
    for en_matrix in enumerate(matrix_list):
        pprint(en_matrix)

    operation_key = operations()
    # what operation do you want to do?
    if operation_key == "P":
        product = dot_product_matrix(matrix_list)
        pprint(product)
        # latex_dot_product(matrix_list)
        with open("output.txt", "a") as f:
            f.write("\n\n$="+ latex(product) + "$")
    
    elif operation_key == "S":
        sum_sub, latex_operation = add_subtract_matrix(matrix_list)
        pprint(sum_sub)
        for matrix in latex_operation:
            with open("output.txt", "a") as f:
                f.write("$"+ latex(matrix) + "$")
        with open("output.txt", "a") as f:
            f.write("\n\n$="+ latex(sum_sub) + "$")
    
    else:
        print("Error in input")
    
if __name__ == "__main__":
    main()



