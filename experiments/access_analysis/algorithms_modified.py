from collections import defaultdict

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

def smawk_with_lookup(num_rows, num_columns, lookup_function):
    if num_rows == 0 or num_columns == 0:
        return None, {}

    minima = [None] * num_rows
    accessed_counts = defaultdict(int)

    # Wrap lookup function to count matrix accesses
    def track(i, j):
        accessed_counts[(i, j)] += 1
        return lookup_function(i, j)

    # Base Case
    if num_rows == 1:
        min_value = track(0, 0)
        min_column = 0
        for j in range(1, num_columns):
            if track(0, j) < min_value:
                min_value = track(0, j)
                min_column = j
        minima[0] = min_column
        return minima, accessed_counts

    # Reduce
    if num_columns > num_rows:
        stack = []
        for j in range(num_columns):
            while stack and track(len(stack) - 1, stack[-1]) > track(len(stack) - 1, j):
                stack.pop()
            if len(stack) < num_rows:
                stack.append(j)
        reduced_columns = stack

        # Recursive SMAWK Call (on reduced column set)
        def reduced_lookup(i, j):
            return track(i, reduced_columns[j])

        reduced_minima, sub_counts = smawk_with_lookup(num_rows, len(reduced_columns), reduced_lookup)
        for key, val in sub_counts.items():
            accessed_counts[(key[0], reduced_columns[key[1]])] += val

        for i in range(num_rows):
            minima[i] = reduced_columns[reduced_minima[i]]

    # Interpolate
    else:
        even_rows = list(range(1, num_rows, 2))
        odd_rows = list(range(0, num_rows, 2))

        # Recursive SMAWK Call (on even-indexed rows)
        def even_lookup(i, j):
            return track(even_rows[i], j)

        reduced_minima, sub_counts = smawk_with_lookup(len(even_rows), num_columns, even_lookup)
        for key, val in sub_counts.items():
            accessed_counts[(even_rows[key[0]], key[1])] += val

        for idx, row in enumerate(even_rows):
            minima[row] = reduced_minima[idx]

        # Find minima for odd-indexed rows via linear search
        for row in odd_rows:
            lower_bound = minima[row - 1] if row > 0 else 0
            upper_bound = minima[row + 1] if row + 1 < num_rows else num_columns - 1
            min_value = track(row, lower_bound)
            min_column = lower_bound
            for j in range(lower_bound + 1, upper_bound + 1):
                if track(row, j) < min_value:
                    min_value = track(row, j)
                    min_column = j
            minima[row] = min_column

    return minima, accessed_counts

def proxy_problem_with_access_tracking(n, m, weights, distances):
    D, W, X, Y = preprocess_sums(n, distances, weights)

    # Initialize DP Table
    F = [[float("inf")] * (m+2) for _ in range(n+2)]
    F[0][0] = 0
    global_accessed = defaultdict(int) # Track all accessed (i,k) entries

    for j in range(1, m+2):
        def lookup(i, k):
            if i >= k or k < 1:
                return float("inf")
            return F[i][j-1] + Y[0] - Y[k] - X[i] + D[i] * W[k]

        # Apply SMAWK
        minima, accessed = smawk_with_lookup(n+2, n+1, lookup)

        # Accumulate all matrix accesses
        for (i, k), count in accessed.items():
            global_accessed[(i, k)] += count

        for i in range(n+2):
            k = minima[i]
            if k is not None:
                F[i][j] = lookup(i, k)

    # Count total and unique accesses
    total_access = sum(global_accessed.values())
    unique_access = len(global_accessed)
    return unique_access, total_access
