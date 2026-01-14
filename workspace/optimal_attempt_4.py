import sys

def solve():
    """
    Solves a single test case for the Nim Sum Dim Sum problem.
    """
    try:
        line = sys.stdin.readline()
        if not line: return
        N = int(line)
        S = sys.stdin.readline().strip()
    except (IOError, ValueError):
        return

    count_A = 0
    for char in S:
        if char == 'A':
            count_A += 1
    
    count_B = N - count_A

    if count_A >= count_B:
        return "Alice"
    else:
        return "Bob"

def main():
    """
    Main function to handle multiple test cases.
    """
    try:
        T_str = sys.stdin.readline()
        if not T_str: return
        T = int(T_str)
        for i in range(1, T + 1):
            winner = solve()
            if winner is not None:
                print(f"Case #{i}: {winner}")
    except (IOError, ValueError):
        return

if __name__ == "__main__":
    main()