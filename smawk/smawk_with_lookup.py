"""
Finds the column index of the minimum value in each row of a totally monotone matrix.

Preconditions:
    - `matrix` must be totally monotone

Parameters:
    num_rows (int): Number of rows in the matrix.
    num_columns (int): Number of columns in the matrix.
    lookup_function (Callable[[int, int], float]): Function that returns the value at (i, j).

Returns:
    List[int]: A list where the i-th entry is the column index 
                of the minimum element in row i.
"""

def smawk_with_lookup(num_rows, num_columns, lookup_function):
    if num_rows == 0 or num_columns == 0:
        return None
    
    minima = [None] * num_rows # will store the column index of row minimum for each row
    
    # Base case
    if num_rows == 1:
        min_value = lookup_function(0, 0)
        min_column = 0
        for j in range(1, num_columns):
            if lookup_function(0, j) < min_value:
                min_value = lookup_function(0, j)
                min_column = j
        minima[0] = min_column
        return minima
    
    # Reuce
    if num_columns > num_rows:
        reduced_columns = []
        stack = []
        for j in range(num_columns):
            while stack and lookup_function(len(stack) - 1, stack[-1]) > lookup_function(len(stack) - 1, j):
                stack.pop()
            if len(stack) < num_rows:
                stack.append(j)
        reduced_columns = stack
        
        # Define reduced lookup on reduced column set
        def reduced_lookup(i, j):
            return lookup_function(i, reduced_columns[j])
        
        # Recursive SMAWK Call on reduced matrix
        reduced_minima = smawk_with_lookup(num_rows, len(reduced_columns), reduced_lookup)
        
        # Map reduced minima back to original column indices
        for i in range(num_rows):
            minima[i] = reduced_columns[reduced_minima[i]]

    # Interpolate
    else:
        even_rows = list(range(1, num_rows, 2))
        odd_rows = list(range(0, num_rows, 2))
        
        # Restrict problem to even-indexed rows
        def even_lookup(i, j):
            return lookup_function(even_rows[i], j)
        
        # Recursive SMAWK Call on even rows
        reduced_minima = smawk_with_lookup(len(even_rows), num_columns, even_lookup)
        
        # Map reduced minima back to original column indices
        for idx, row in enumerate(even_rows):
            minima[row] = reduced_minima[idx]
        
        # Compute minima for odd rows vial linear search in restricted area
        for row in odd_rows:
            lower_bound = minima[row - 1] if row > 0 else 0
            upper_bound = minima[row + 1] if row + 1 < num_rows else num_columns - 1
            min_value = lookup_function(row, lower_bound)
            min_column = lower_bound
            for j in range(lower_bound + 1, upper_bound + 1):
                if lookup_function(row, j) < min_value:
                    min_value = lookup_function(row, j)
                    min_column = j
            minima[row] = min_column
            
    return minima

if __name__ == "__main__":
    # Example values
    matrix = [
        [25, 21, 13, 10, 20, 13, 19, 35, 37, 41, 58, 66, 82, 99, 124, 133, 156, 178],
        [42, 35, 26, 20, 29, 21, 25, 37, 36, 39, 56, 64, 76, 91, 116, 125, 146, 164],
        [57, 48, 35, 28, 33, 24, 28, 40, 37, 37, 54, 61, 72, 83, 107, 113, 131, 146],
        [78, 65, 51, 42, 44, 35, 38, 48, 42, 42, 55, 61, 70, 80, 100, 106, 120, 135],
        [90, 76, 58, 48, 49, 39, 42, 48, 39, 35, 47, 51, 56, 63, 80, 86, 97, 110],
        [103, 85, 67, 56, 55, 44, 44, 49, 39, 33, 41, 44, 49, 56, 71, 75, 84, 96],
        [123, 105, 86, 75, 73, 59, 57, 62, 51, 44, 50, 52, 55, 59, 72, 74, 80, 92],
        [142, 123, 100, 86, 82, 65, 61, 62, 50, 43, 47, 45, 46, 46, 58, 59, 65, 73],
        [151, 130, 104, 88, 80, 59, 52, 49, 37, 29, 29, 24, 23, 20, 28, 25, 31, 39]
    ]

    num_rows = len(matrix)
    num_columns = len(matrix[0])

    def lookup(i, j):
        return matrix[i][j]

    minima_indices = smawk_with_lookup(num_rows, num_columns, lookup)

    for i, col in enumerate(minima_indices):
        val = matrix[i][col]
        print(f"Row {i:2}: min at column {col:2} (value = {val})")
