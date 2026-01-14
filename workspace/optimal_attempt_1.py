import sys
from collections import deque

def solve():
    """
    Solves the ladder relocation problem using Breadth-First Search (BFS).
    """
    try:
        line = sys.stdin.readline()
        if not line:
            return
        M, N = map(int, line.split())
        grid = [sys.stdin.readline().split() for _ in range(M)]
    except (IOError, ValueError):
        return

    source_coords = []
    dest_coords = []
    for r in range(M):
        for c in range(N):
            if grid[r][c] == 'l':
                source_coords.append((r, c))
                grid[r][c] = 'E'
            elif grid[r][c] == 'L':
                dest_coords.append((r, c))
                grid[r][c] = 'E'

    if not source_coords:
        print(0 if not dest_coords else "Impossible")
        return

    length = len(source_coords)
    
    source_coords.sort()
    dest_coords.sort()

    if source_coords == dest_coords:
        print(0)
        return

    # State: (row, col, orientation), where orientation is 0 for horizontal, 1 for vertical
    start_r, start_c = source_coords[0]
    start_o = 0 if length <= 1 or source_coords[0][0] == source_coords[1][0] else 1
    start_state = (start_r, start_c, start_o)

    end_r, end_c = dest_coords[0]
    end_o = 0 if length <= 1 or dest_coords[0][0] == dest_coords[1][0] else 1
    end_state = (end_r, end_c, end_o)

    q = deque([(start_state, 0)])
    visited = {start_state}

    while q:
        (r, c, o), dist = q.popleft()

        if (r, c, o) == end_state:
            print(dist)
            return

        # 1. Translations
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            new_state = (nr, nc, o)

            if new_state in visited:
                continue

            valid_pos = True
            if o == 0:  # horizontal
                if not (0 <= nr < M and 0 <= nc < N and nc + length - 1 < N):
                    valid_pos = False
                else:
                    for k in range(length):
                        if grid[nr][nc + k] == 'B':
                            valid_pos = False
                            break
            else:  # vertical
                if not (0 <= nr < M and 0 <= nc < N and nr + length - 1 < M):
                    valid_pos = False
                else:
                    for k in range(length):
                        if grid[nr + k][nc] == 'B':
                            valid_pos = False
                            break
            
            if valid_pos:
                visited.add(new_state)
                q.append((new_state, dist + 1))

        # 2. Rotations
        new_o = 1 - o
        for i in range(length):  # pivot index
            if o == 0:  # horizontal -> vertical
                sq_r, sq_c = r - i, c
                new_r, new_c = r - i, c + i
            else:  # vertical -> horizontal
                sq_r, sq_c = r, c - i
                new_r, new_c = r + i, c - i
            
            new_state = (new_r, new_c, new_o)
            if new_state in visited:
                continue

            valid_area = True
            for row_offset in range(length):
                for col_offset in range(length):
                    check_r, check_c = sq_r + row_offset, sq_c + col_offset
                    if not (0 <= check_r < M and 0 <= check_c < N and grid[check_r][check_c] != 'B'):
                        valid_area = False
                        break
                if not valid_area:
                    break
            
            if valid_area:
                visited.add(new_state)
                q.append((new_state, dist + 1))

    print("Impossible")

solve()