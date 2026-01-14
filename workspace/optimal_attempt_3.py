import sys

def solve():
    """
    Solves a single test case for the Nim Sum Dim Sum problem.
    """
    try:
        # Read N, but it's not strictly necessary for this logic.
        # Reading it ensures we consume the input correctly.
        n_str = sys.stdin.readline()
        if not n_str.strip():  # Handle potential blank lines
            n_str = sys.stdin.readline()
        N = int(n_str)
        
        S = sys.stdin.readline().strip()
    except (IOError, ValueError):
        return

    count_A = 0
    count_B = 0
    for char in S:
        if char == 'A':
            count_A += 1
        else:
            count_B += 1

    if count_A >= count_B:
        print("Alice")
    else:
        print("Bob")

def main():
    """
    Main function to handle multiple test cases.
    """
    try:
        t_str = sys.stdin.readline()
        if not t_str: return
        T = int(t_str)
        for i in range(1, T + 1):
            print(f"Case #{i}: ", end="")
            solve()
    except (IOError, ValueError):
        return

if __name__ == "__main__":
    main()