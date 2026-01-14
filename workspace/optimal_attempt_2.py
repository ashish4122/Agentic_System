import sys

class SegmentTreeMax:
    def __init__(self, data):
        self.n = len(data)
        self.data = data
        self.tree = [(-float('inf'), -1)] * (4 * self.n)
        if self.n > 0:
            self.build(0, 0, self.n - 1)

    def build(self, node, start, end):
        if start == end:
            self.tree[node] = self.data[start]
            return
        mid = (start + end) // 2
        self.build(2 * node + 1, start, mid)
        self.build(2 * node + 2, mid + 1, end)
        self.tree[node] = max(self.tree[2 * node + 1], self.tree[2 * node + 2])

    def query(self, l, r):
        if l > r:
            return (-float('inf'), -1)
        return self._query(0, 0, self.n - 1, l, r)

    def _query(self, node, start, end, l, r):
        if r < start or end < l:
            return (-float('inf'), -1)
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        p1 = self._query(2 * node + 1, start, mid, l, r)
        p2 = self._query(2 * node + 2, mid + 1, end, l, r)
        return max(p1, p2)

class SegmentTreeMin:
    def __init__(self, data):
        self.n = len(data)
        self.data = data
        self.tree = [(float('inf'), -1)] * (4 * self.n)
        if self.n > 0:
            self.build(0, 0, self.n - 1)

    def build(self, node, start, end):
        if start == end:
            self.tree[node] = self.data[start]
            return
        mid = (start + end) // 2
        self.build(2 * node + 1, start, mid)
        self.build(2 * node + 2, mid + 1, end)
        self.tree[node] = min(self.tree[2 * node + 1], self.tree[2 * node + 2])

    def query(self, l, r):
        if l > r:
            return (float('inf'), -1)
        return self._query(0, 0, self.n - 1, l, r)

    def _query(self, node, start, end, l, r):
        if r < start or end < l:
            return (float('inf'), -1)
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        p1 = self._query(2 * node + 1, start, mid, l, r)
        p2 = self._query(2 * node + 2, mid + 1, end, l, r)
        return min(p1, p2)

def solve():
    try:
        line = sys.stdin.readline()
        if not line.strip(): line = sys.stdin.readline()
        N = int(line)
        S = sys.stdin.readline().strip()
    except (IOError, ValueError):
        return ""

    A_indices = [i for i, c in enumerate(S) if c == 'A']
    B_indices = [i for i, c in enumerate(S) if c == 'B']
    
    CA = [0] * (N + 1)
    CB = [0] * (N + 1)
    for i in range(N):
        CA[i+1] = CA[i] + (1 if S[i] == 'A' else 0)
        CB[i+1] = CB[i] + (1 if S[i] == 'B' else 0)

    SA = [CB[i] - CA[i] for i in range(N + 1)]
    SB = [CA[i] - CB[i] for i in range(N + 1)]

    SA_A_pairs = [(SA[i], -i) for i in A_indices]
    A_seg_tree = SegmentTreeMax(SA_A_pairs)

    SB_B_pairs = [(SB[i+1], i) for i in B_indices]
    B_seg_tree = SegmentTreeMin(SB_B_pairs)

    l, r = 0, N - 1
    a_ptr_l, a_ptr_r = 0, len(A_indices) - 1
    b_ptr_l, b_ptr_r = 0, len(B_indices) - 1
    
    turn = 0
    last_eater = ""

    while l <= r:
        while a_ptr_l <= a_ptr_r and A_indices[a_ptr_l] < l: a_ptr_l += 1
        while a_ptr_l <= a_ptr_r and A_indices[a_ptr_r] > r: a_ptr_r -= 1
        while b_ptr_l <= b_ptr_r and B_indices[b_ptr_l] < l: b_ptr_l += 1
        while b_ptr_l <= b_ptr_r and B_indices[b_ptr_r] > r: b_ptr_r -= 1

        has_A = a_ptr_l <= a_ptr_r
        has_B = b_ptr_l <= b_ptr_r

        if not has_A and not has_B: break

        if turn == 0:
            if not has_A:
                turn = 1
                continue
            
            _, neg_i = A_seg_tree.query(a_ptr_l, a_ptr_r)
            i_star = -neg_i
            
            l = i_star + 1
            last_eater = "Alice"
            turn = 1
        else:
            if not has_B:
                turn = 0
                continue
            
            _, j_star = B_seg_tree.query(b_ptr_l, b_ptr_r)
            
            r = j_star - 1
            last_eater = "Bob"
            turn = 0
            
    return last_eater

def main():
    sys.setrecursionlimit(2 * 10**6)
    try:
        T_str = sys.stdin.readline()
        if not T_str: return
        T = int(T_str)
        for i in range(1, T + 1):
            result = solve()
            if result:
                print(f"Case #{i}: {result}")
    except (IOError, ValueError):
        return

if __name__ == "__main__":
    main()