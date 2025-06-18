def preprocess_sums(n, distances, weights):
    distances = [0] + distances + [0]
    weights = [0] + weights + [0]
    D = [0] * (n+2)
    W = [weights[n]] * (n+2)
    X = [0] * (n+2)
    Y = [0] *(n+2)

    for j in range(1, n+2):
        D[j] = D[j-1] + distances[j] 

    for j in range(n, -1, -1):
        W[j] = W[j+1] + weights[j]

    for j in range(1, n+2):
        X[j] = X[j-1] + distances[j] * W[j]

    Y[n+1] = weights[n+1] * D[n+1]
    for j in range(n, -1, -1):
        Y[j] = Y[j+1] + weights[j]*D[j]

    return D, W, X, Y

def proxy_problem_unoptimized(n, m, weights, distances):
    D,W,X,Y = preprocess_sums(n, distances, weights)

    # Initialize comparison counter
    comparison_count = 0
    
    def a(i,j):
        return Y[0]-Y[j]-X[i]+D[i]*W[j]

    F = [[float('inf') for _ in range(m+2)] for _ in range(n+2)]
    for j in range(1, n+2):
        F[j][1] = a(0,j) 
    for k in range(2, m+2):
        F[1][k] = 0  

    for k in range(2, m+2):
        for j in range(2, n+2):
            F[j][k] = float('inf')
            for i in range(1, j):
                comparison_count += 1  # Count comparisons
                F[j][k] = min(F[j][k], F[i][k-1] + a(i,j))

    # Return result and comparison count
    return F[n+1][m+1], comparison_count

def smawk_with_lookup(num_rows, num_columns, lookup_function):
    if num_rows == 0 or num_columns == 0:
        return None
        
    minima = [None] * num_rows

    # Initialize comparison counter
    comparison_count = 0
    
    # Base Case
    if num_rows == 1:
        min_value = lookup_function(0, 0)
        min_column = 0
        for j in range(1, num_columns):
            comparison_count += 1  # Count comparisons
            if lookup_function(0, j) < min_value:
                min_value = lookup_function(0, j)
                min_column = j
        minima[0] = min_column

        # Return result and comparison count
        return minima, comparison_count
    
    # Reduce
    if num_columns > num_rows:
        reduced_columns = []
        stack = []
        for j in range(num_columns):
            while stack and lookup_function(len(stack) - 1, stack[-1]) > lookup_function(len(stack) - 1, j):
                stack.pop()
            if len(stack) < num_rows:
                stack.append(j)
        reduced_columns = stack
        
        # Recursive SMAWK Call (on reduced column set)
        def reduced_lookup(i, j):
            return lookup_function(i, reduced_columns[j])
            
        reduced_minima, sub_comparisons = smawk_with_lookup(num_rows, len(reduced_columns), reduced_lookup)
        comparison_count += sub_comparisons
        
        for i in range(num_rows):
            minima[i] = reduced_columns[reduced_minima[i]]

    # Interpolate
    else:
        even_rows = list(range(1, num_rows, 2))
        odd_rows = list(range(0, num_rows, 2))
        
        # Recursive SMAWK Call (on even-indexed rows)
        def even_lookup(i, j):
            return lookup_function(even_rows[i], j)
            
        reduced_minima, sub_comparisons = smawk_with_lookup(len(even_rows), num_columns, even_lookup)
        comparison_count += sub_comparisons
        
        for idx, row in enumerate(even_rows):
            minima[row] = reduced_minima[idx]
        
        # Find minima for odd-indexed rows via linear search
        for row in odd_rows:
            lower_bound = minima[row - 1] if row > 0 else 0
            upper_bound = minima[row + 1] if row + 1 < num_rows else num_columns - 1
            min_value = lookup_function(row, lower_bound)
            min_column = lower_bound
            for j in range(lower_bound + 1, upper_bound + 1):
                comparison_count += 1  # Count comparisons
                if lookup_function(row, j) < min_value:
                    min_value = lookup_function(row, j)
                    min_column = j
            minima[row] = min_column
    
    # Return result and comparison counter
    return minima, comparison_count

def preprocess_sums(n, distances, weights):
    distances = [0] + distances + [0]
    weights = [0] + weights + [0]
    D = [0] * (n+2)
    W = [weights[n]] * (n+2)
    X = [0] * (n+2)
    Y = [0] *(n+2)

    for j in range(1, n+2):
        D[j] = D[j-1] + distances[j]  # Cumulative sum of distances

    for j in range(n, -1, -1):
        W[j] = W[j+1] + weights[j]

    for j in range(1, n+2):
        X[j] = X[j-1] + distances[j] * W[j]

    Y[n+1] = weights[n+1] * D[n+1]
    for j in range(n, -1, -1):
        Y[j] = Y[j+1] + weights[j]*D[j]

    return D, W, X, Y

def proxy_problem(n, m, weights, distances):
    D, W, X, Y = preprocess_sums(n, distances, weights)
    total_comparison_count = 0  # Initialize comparison counter

    def a(i, j):
        return Y[0] - Y[j] - X[i] + D[i] * W[j]
    
    # Initialize DP Table
    F = [[float('inf') for _ in range(m+2)] for _ in range(n+2)]

    for j in range(0, n+2):
        F[j][1] = a(0, j)
    for k in range(0, m+2):
        F[1][k] = 0

    def lookup_b(j, i):
        if i >= j or j < 2: 
            return float('inf')
        return F[i][k-1] + a(i, j)
    
    # Compute F[j, k] iteratively using smawk
    for k in range(2, m+2):
        minima, comparison_count = smawk_with_lookup(n+2, n+2, lookup_b)
        total_comparison_count += comparison_count
        for j in range(2, n+2):
            F[j][k] = lookup_b(j, minima[j])

    # Return result and total comparison count
    return F[n+1][m+1], total_comparison_count 
