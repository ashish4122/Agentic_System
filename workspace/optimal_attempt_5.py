import sys

def solve():
    """
    Solves a single test case.
    """
    try:
        line = sys.stdin.readline()
        if not line: return None
        N = int(line)
        S = sys.stdin.readline().strip()
    except (IOError, ValueError):
        return None

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
        line = sys.stdin.readline()
        if not line: return
        T = int(line)
        for i in range(1, T + 1):
            result = solve()
            if result is None: break
            print(f"Case #{i}: {result}")
    except (IOError, ValueError):
        pass

if __name__ == "__main__":
    main()