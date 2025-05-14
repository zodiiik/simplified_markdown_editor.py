class MatrixProcessor:
    def __init__(self):
        self.menu_options = {
            1: ("Add matrices", self.add_matrices),
            2: ("Multiply matrix by a constant", self.multiply_by_constant),
            3: ("Multiply matrices", self.multiply_matrices),
            4: ("Transpose matrix", self.transpose_matrix),
            5: ("Calculate a determinant", self.calculate_determinant),
            6: ("Inverse matrix", self.inverse_matrix),
            0: ("Exit", self.exit_program)
        }
        self.transpose_options = {
            1: ("Main diagonal", self.transpose_main),
            2: ("Side diagonal", self.transpose_side),
            3: ("Vertical line", self.transpose_vertical),
            4: ("Horizontal line", self.transpose_horizontal)
        }

    def run(self):
        while True:
            self.print_menu()
            choice = self.get_choice(len(self.menu_options) - 1)
            if choice == 0:
                break
            self.menu_options[choice][1]()

    def print_menu(self):
        print("\n".join(f"{key}. {value[0]}" for key, value in self.menu_options.items()))

    def get_choice(self, max_option):
        while True:
            try:
                choice = int(input("Your choice: > "))
                if 0 <= choice <= max_option:
                    return choice
                print(f"Please enter a number between 0 and {max_option}")
            except ValueError:
                print("Please enter a valid number")

    def read_matrix(self, prompt="", with_size=True):
        if prompt:
            print(prompt)
        if with_size:
            rows, cols = map(int, input("Enter size of matrix: > ").split())
            print("Enter matrix:")
        else:
            rows = len(self.matrix)
            cols = len(self.matrix[0]) if rows > 0 else 0

        matrix = []
        for _ in range(rows):
            row = list(map(float, input("> ").split()))
            if with_size and len(row) != cols:
                raise ValueError("Invalid number of columns")
            matrix.append(row)
        return matrix

    def print_matrix(self, matrix):
        for row in matrix:
            print(" ".join(f"{num:.2f}".rstrip('0').rstrip('.') if isinstance(num, float) else str(num) for num in row))

    def add_matrices(self):
        print("Enter first matrix:")
        matrix_a = self.read_matrix()
        print("Enter second matrix:")
        matrix_b = self.read_matrix()

        if len(matrix_a) != len(matrix_b) or len(matrix_a[0]) != len(matrix_b[0]):
            print("ERROR")
            return

        result = [[matrix_a[i][j] + matrix_b[i][j] for j in range(len(matrix_a[0])) for i in range(len(matrix_a))]
        print("The result is:")
        self.print_matrix(result)

    def multiply_by_constant(self):
        matrix = self.read_matrix()
        constant = float(input("Enter constant: > "))
        
        result = [[element * constant for element in row] for row in matrix]
        print("The result is:")
        self.print_matrix(result)

    def multiply_matrices(self):
        print("Enter first matrix:")
        matrix_a = self.read_matrix()
        print("Enter second matrix:")
        matrix_b = self.read_matrix()

        if len(matrix_a[0]) != len(matrix_b):
            print("The operation cannot be performed.")
            return

        result = [[sum(a * b for a, b in zip(row_a, col_b)) 
                  for col_b in zip(*matrix_b)] for row_a in matrix_a]
        print("The result is:")
        self.print_matrix(result)

    def transpose_matrix(self):
        print("\n".join(f"{key}. {value[0]}" for key, value in self.transpose_options.items()))
        choice = self.get_choice(len(self.transpose_options))
        self.matrix = self.read_matrix()
        self.transpose_options[choice][1]()
        print("The result is:")
        self.print_matrix(self.result)

    def transpose_main(self):
        self.result = [[self.matrix[j][i] for j in range(len(self.matrix))] 
                      for i in range(len(self.matrix[0]))]

    def transpose_side(self):
        self.result = [[self.matrix[-j-1][-i-1] for j in range(len(self.matrix))] 
                      for i in range(len(self.matrix[0]))]

    def transpose_vertical(self):
        self.result = [row[::-1] for row in self.matrix]

    def transpose_horizontal(self):
        self.result = self.matrix[::-1]

    def calculate_determinant(self):
        matrix = self.read_matrix()
        if len(matrix) != len(matrix[0]):
            print("Matrix must be square to calculate determinant")
            return

        det = self.determinant(matrix)
        print("The result is:")
        print(int(det) if det.is_integer() else det)

    def determinant(self, matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        if len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

        det = 0
        for c in range(len(matrix)):
            minor = [row[:c] + row[c+1:] for row in matrix[1:]]
            det += (-1) ** c * matrix[0][c] * self.determinant(minor)
        return det

    def inverse_matrix(self):
        matrix = self.read_matrix()
        if len(matrix) != len(matrix[0]):
            print("Matrix must be square to find inverse")
            return

        det = self.determinant(matrix)
        if det == 0:
            print("This matrix doesn't have an inverse.")
            return

        if len(matrix) == 1:
            inverse = [[1 / matrix[0][0]]]
        else:
            cofactors = []
            for r in range(len(matrix)):
                cofactor_row = []
                for c in range(len(matrix)):
                    minor = [row[:c] + row[c+1:] for row in (matrix[:r]+matrix[r+1:])]
                    cofactor_row.append(((-1) ** (r + c)) * self.determinant(minor))
                cofactors.append(cofactor_row)
            cofactors = [[cofactors[j][i] for j in range(len(cofactors))] for i in range(len(cofactors[0]))]
            inverse = [[element / det for element in row] for row in cofactors]

        print("The result is:")
        self.print_matrix(inverse)

    def exit_program(self):
        pass

if __name__ == "__main__":
    processor = MatrixProcessor()
    processor.run()