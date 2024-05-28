class Node:
    __slots__ = "row", "col", "data", "next"

    def __init__(self, row=0, col=0, data=0, next=None):
        self.row = row
        self.col = col
        self.data = data
        self.next = next

class SparseMatrix:
    def __init__(self, numRows=None, numCols=None, matrixFilePath=None):
        self.head = None
        self.temp = None
        self.numRows = numRows
        self.numCols = numCols
        self.size = 0
        if matrixFilePath:
            self.load_matrix(matrixFilePath)

    def __len__(self):
        return self.size

    def isempty(self):
        return self.size == 0

    def create_new_node(self, row, col, data):
        newNode = Node(row, col, data, None)
        if self.isempty():
            self.head = newNode
        else:
            self.temp.next = newNode
        self.temp = newNode
        self.size += 1

    def load_matrix(self, matrixFilePath):
        try:
            with open(matrixFilePath, 'r') as file:
                lines = file.readlines()
                self.numRows = int(lines[0].split('=')[1].strip())
                self.numCols = int(lines[1].split('=')[1].strip())
                self.head = None
                self.temp = None
                self.size = 0
                for line in lines[2:]:
                    line = line.strip()
                    if line:
                        if line.startswith('(') and line.endswith(')'):
                            row, col, value = map(int, line[1:-1].split(','))
                            if value != 0:
                                self.create_new_node(row, col, value)
                        else:
                            raise ValueError("Input file has wrong format")
        except Exception as e:
            raise ValueError("Input file has wrong format") from e

    def getElement(self, row, col):
        temp = self.head
        while temp:
            if temp.row == row and temp.col == col:
                return temp.data
            temp = temp.next
        return 0

    def setElement(self, row, col, value):
        temp = self.head
        prev = None
        while temp:
            if temp.row == row and temp.col == col:
                if value == 0:
                    if prev:
                        prev.next = temp.next
                    else:
                        self.head = temp.next
                    self.size -= 1
                else:
                    temp.data = value
                return
            prev = temp
            temp = temp.next
        if value != 0:
            self.create_new_node(row, col, value)

    def add(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions do not match for addition")

        result = SparseMatrix(self.numRows, self.numCols)
        temp = self.head
        while temp:
            result.setElement(temp.row, temp.col, temp.data)
            temp = temp.next
        temp = other.head
        while temp:
            result.setElement(temp.row, temp.col, result.getElement(temp.row, temp.col) + temp.data)
            temp = temp.next
        return result

    def subtract(self, other):
        if self.numRows != other.numRows or self.numCols != other.numCols:
            raise ValueError("Matrix dimensions do not match for subtraction")

        result = SparseMatrix(self.numRows, self.numCols)
        temp = self.head
        while temp:
            result.setElement(temp.row, temp.col, temp.data)
            temp = temp.next
        temp = other.head
        while temp:
            result.setElement(temp.row, temp.col, result.getElement(temp.row, temp.col) - temp.data)
            temp = temp.next
        return result

    def multiply(self, other):
        if self.numCols != other.numRows:
            raise ValueError("Matrix dimensions do not match for multiplication")

        result = SparseMatrix(self.numRows, other.numCols)
        tempA = self.head
        while tempA:
            tempB = other.head
            while tempB:
                if tempA.col == tempB.row:
                    result.setElement(tempA.row, tempB.col, result.getElement(tempA.row, tempB.col) + tempA.data * tempB.data)
                tempB = tempB.next
            tempA = tempA.next
        return result

    def print_matrix(self):
        temp = self.head
        while temp:
            print(f"({temp.row}, {temp.col}, {temp.data})")
            temp = temp.next

def main():
    import sys
    if len(sys.argv) != 4:
        print("Usage: python sparse_matrix.py <matrix1> <matrix2> <operation>")
        return

    matrix1_path = sys.argv[1]
    matrix2_path = sys.argv[2]
    operation = sys.argv[3]

    try:
        matrix1 = SparseMatrix(matrixFilePath=matrix1_path)
        matrix2 = SparseMatrix(matrixFilePath=matrix2_path)

        if operation == 'add':
            result = matrix1.add(matrix2)
        elif operation == 'subtract':
            result = matrix1.subtract(matrix2)
        elif operation == 'multiply':
            result = matrix1.multiply(matrix2)
        else:
            print("Invalid operation. Choose from 'add', 'subtract', 'multiply'.")
            return

        result.print_matrix()

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
