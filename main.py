from sympy import Matrix, latex, pprint, init_printing, shape
init_printing(use_unicode=True)

class MatrixInputValidator:
    """This module verifies shape entered by user and number of unique shapes
    """
    @staticmethod
    def validate_positive_input(prompt):
        """Decorator to validate positive integer inputs."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                while True:
                    value = input(prompt)
                    try:
                        value = int(value)
                        if value > 0:
                            return func(value, *args, **kwargs)
                        else:
                            print("Please enter a positive integer.")
                    except ValueError:
                        print("Invalid input. Please enter an integer.")
            return wrapper
        return decorator

    @validate_positive_input("No. of unique matrices undergoing operations: ")
    def get_matrix_count(value):
        return value

    @validate_positive_input("No. of rows: ")
    def get_rows(value):
        return value

    @validate_positive_input("No. of columns: ")
    def get_columns(value):
        return value

class MatrixBuilder:
    """
    A module that builds n*n matrix using valid datatype
    """
    def __init__(self):
        self.matrices = []

    def create_matrix(self, rows, columns):
        """This function asks user values input elements at every place
        """
        matrix = []
        for i in range(rows):
            row = []
            for j in range(columns):
                entry = input(f"Enter value for Row {i+1}, Column {j+1}: ")
                row.append(entry)
            matrix.append(row)
        return Matrix(matrix)

    def build_matrix(self):
        """
        Builds the matrix and stores it in the list for easy user experience
        """
        matrix_input_validator = MatrixInputValidator()
        matrix_count = matrix_input_validator.get_matrix_count()
        for _ in range(matrix_count):
            rows = matrix_input_validator.get_rows()
            columns = matrix_input_validator.get_columns()
            matrix = self.create_matrix(rows, columns)
            self.matrices.append(matrix)
        return self.matrices

    def display_matrix(self):
        """This function enumerates the matrix so that user can see what matrix they want to use to perform operations
        """
        for en_matrix in enumerate(self.matrices):
            pprint(en_matrix)

class MatrixOperations:
    """A module that handles user input of Matrix Operaitons
    """
    def __init__(self, builder):
        self.builder = builder

    def add_subtract_matrix(self):
        """
        Sum/Subtracts n numbers a*b matrix with same dimensions together
        Additional feature for latex support
        """
        matrix_list = self.builder.matrices
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

        pprint(latex_operation)
        pprint(operation_sum_sub)

        return operation_sum_sub, latex_operation

    def dot_product_matrix(self):
        """
        Dot product of n numbers of a*b matrix with proper dimension
        Latex based output with intermediate steps and final solution
        """
        matrix_list = self.builder.matrices
        matrix_num = int(input("How many matrix participates in operation? "))

        # latex print of all matrix
        for matrix in matrix_list:
            with open("output.txt", "a", encoding="utf-8") as output_file:
                output_file.write("$"+ latex(matrix) + "$\n")

        with open("output.txt", "a", encoding="utf-8") as output_file:
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
                with open("output.txt", "a", encoding="utf-8") as output_file:
                    output_file.write("\n$" + str(_) + "$")

        print(steps)

        return initialize_product

    def reducedref_matrix(self):
        """
        Reduced Row Echelon Forms of the matrix with intermediate steps support and suffles rows when the first
        element is zero. LaTeX to suffle the row to be initated later.
        """
        matrix_list = self.builder.matrices
        index = int(input("Index of the matrix to rref:: "))
        rref_matrix = matrix_list[index]
        rref_matrix_row, rref_matrix_col = shape(rref_matrix)
        _, pivot = rref_matrix.rref()

        # RREFing even when we have a first row starts at zero (latex left) by row-swap
        if rref_matrix[0,0] == 0:
            for i in range(rref_matrix_row):
                if rref_matrix[i,0] != 0:
                    holder = rref_matrix[0,:]
                    rref_matrix[0,:] = rref_matrix[i,:]
                    rref_matrix[i,:] = holder
                else:
                    continue

        with open("rref.tex", "w", encoding="utf-8") as output_file:
            output_file.write("$$"+ latex(rref_matrix) + "$$\n")

        for i in range(min(rref_matrix_row, rref_matrix_col)):
            if rref_matrix[i,i] == 0:
                pass
            else:
                with open("rref1.tex", "a", encoding="utf-8") as output_file:
                    output_file.write(f"$$\\frac{(1)}{({rref_matrix[i,i]})} R_{{{i+1}}} \\rightarrow R_{{{i+1}}}$$\n")
                rref_matrix[i, :] = (rref_matrix[i,:]/rref_matrix[i,i])

            for j in range(rref_matrix_row):
                if j == i:
                    pass
                else:
                    # Write the operation to the LaTeX file
                    with open("rref1.tex", "a", encoding="utf-8") as output_file:
                        output_file.write(f"$$R_{{{j+1}}} - ({rref_matrix[j,i]}) \\cdot R_{{{i+1}}} \\rightarrow R_{{{j+1}}}$$\n")

                    rref_matrix[j,:] = rref_matrix[j,:] - (rref_matrix[j,i]*rref_matrix[i,:])
                    with open("rref1.tex", "a", encoding="utf-8") as output_file:
                        # output_file.write("$\\longrightarrow$\n")
                        output_file.write("$$"+ latex(rref_matrix) + "$$\n")

        pprint(rref_matrix)

        with open("rref1.tex", "a", encoding="utf-8") as output_file:
            # output_file.write("$\\longrightarrow$\n")
            output_file.write(f"$$Pivot:"+ str(pivot) + "$$\n")

    def rowef_matrix(self):
        """
        Row Echelon forms for the matrix with concept of intermediate steps,
        Full LaTeX support to be initiated soon
        """
        matrix_list = self.builder.matrices
        index = int(input("Index of the matrix to ref:: "))
        ref_matrix = matrix_list[index]
        ref_matrix_row, ref_matrix_col = shape(ref_matrix)

        if ref_matrix[0,0] == 0:
            for i in range(ref_matrix_row):
                if ref_matrix[i,0] != 0:
                    holder = ref_matrix[0,:]
                    ref_matrix[0,:] = ref_matrix[i,:]
                    ref_matrix[i,:] = holder
                else:
                    continue

        for i in range(min(ref_matrix_row, ref_matrix_col)):
            for j in range(i+1,ref_matrix_row):
                if ref_matrix[i,i] != 0:
                    factor = ref_matrix[j,i]/ref_matrix[i,i]
                    ref_matrix[j,:] = ref_matrix[j,:] - (factor * ref_matrix[i,:])

        pprint(ref_matrix)

class OperationKey:
    """
    Operation Key class parse through key catalogue
    """
    def __init__(self, builder):
        self.builder = builder
        self.operations = MatrixOperations(builder)

    def choosekey(self):
        """
        Module to choose what operation user wants to perform
        """
        key = input("Choose Operation Key SUM/SUBTRACT or PRODUCT or RREF or REF [S/P/RR/R]:: ").upper().strip()
        if key in (["S", "P", "RR", "R"]):
            if key == "S":
                self.operations.add_subtract_matrix()
            elif key == "P":
                self.operations.dot_product_matrix()
            elif key == "RR":
                self.operations.reducedref_matrix()
            elif key == "R":
                self.operations.rowef_matrix()
        else:
            print("Wrong Key")

def main():
    """
    Main function class to initialize everything
    """
    builder = MatrixBuilder()
    builder.build_matrix()
    builder.display_matrix()

    MatrixOperations(builder)
    operartionkey = OperationKey(builder)
    operartionkey.choosekey()


if __name__ == "__main__":
    main()
