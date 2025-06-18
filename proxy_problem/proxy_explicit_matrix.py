from smawk.smawk_explicit_matrix import smawk

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


"""
Computes the minimal total latency for placing m proxies among n nodes.

Parameters:
    n (int): Number of nodes (excluding v0)
    m (int): Number of proxies
    weights (List[int]): Request frequency at each node
    distances (List[int]): Distance between consecutive nodes

Returns:
    int: The minimal total latency
"""
def proxy_problem_explicit_matrix(n, m, weights, distances):
    D, W, X, Y = preprocess_sums(n, distances, weights)

    # cost function
    def a(i, j):
        return Y[0] - Y[j] - X[i] + D[i] * W[j]
    
    # Initialize DP table
    F = [[float('inf') for _ in range(m+2)] for _ in range(n+2)]

    # Base cases
    for j in range(0, n+2):
        F[j][1] = a(0, j)

    for k in range(0, m+2):
        F[1][k] = 0

    # Dynamic Programming via SMAWK
    for k in range(2, m+2):

        # Construct M^T
        M = [[float('inf') for _ in range(n+1)] for _ in range(n+2)]

        for j in range(2, n+2):
            for i in range(1, j):
                M[j][i] = F[i][k-1] + a(i, j)

        # Use SMAWK to find row-minima in M^T
        minima = smawk(M)

        # Update DP Table using minima positions
        for j in range(2,n+2):
            F[j][k]= M[j][minima[j]]

    return F[n+1][m+1]


if __name__ == "__main__":
    # Example values
    n = 7  # Number of nodes (including v0)
    m = 2  # Number of proxies
    weights = [10, 15, 20, 25, 5, 8, 30]  # Weights of the nodes
    distances = [2, 3, 5, 4, 1, 3, 2]  # Distances between consecutive nodes

    result1 = proxy_problem_explicit_matrix(n, 0, weights, distances)
    result2 = proxy_problem_explicit_matrix(n, m, weights, distances)

    print(f"Minimal total latency (m=2): {result1}")
    print(f"Minimal total latency with no proxies: {result2}")