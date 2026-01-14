import sys
from collections import deque

def run_solution():
    try:
        line = sys.stdin.readline()
        if not line.strip():
            return
        M, N = map(int, line.split())
        grid = [sys.stdin.readline().split() for _ in range(M)]
    except (ValueError, IndexError):
        return

    source_coords = []
    dest_coords = []
    for r in range(M):
        for c in range(N):
            if grid[r][c] == 'l':
                source_coords.append((r, c))
            elif grid[r][c] == 'L':
                dest_coords.append((r, c))

    if not source_coords or not dest_coords:
        print("Impossible")
        return

    length = len(source_coords)
    
    source_coords.sort()
    dest_coords.sort()

    start_r, start_c = source_coords[0]
    start_orient = 0 if source_coords[0][0] == source_coords[1][0] else 1

    target_r, target_c = dest_coords[0]
    target_orient = 0 if dest_coords[0][0] == dest_coords[1][0] else 1

    q = deque([(start_r, start_c, start_orient, 0)])
    visited = set([(start_r, start_c, start_orient)])
    
    target_state = (target_r, target_c, target_orient)

    while q:
        r, c, orient, steps = q.popleft()

        if (r, c, orient) == target_state:
            print(steps)
            return

        # Try Translations
        dr = [-1, 1, 0, 0]
        dc = [0, 0, -1, 1]
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            new_state = (nr, nc, orient)
            if new_state in visited:
                continue
            is_valid = True
            if orient == 0: # horizontal
                if not (0 <= nr < M and 0 <= nc < N and nc + length - 1 < N):
                    is_valid = False
                else:
                    for k in range(length):
                        if grid[nr][nc + k] == 'B':
                            is_valid = False
                            break
            else: # vertical
                if not (0 <= nr < M and 0 <= nc < N and nr + length - 1 < M):
                    is_valid = False
                else:
                    for k in range(length):
                        if grid[nr + k][nc] == 'B':
                            is_valid = False
                            break
            if is_valid:
                visited.add(new_state)
                q.append((nr, nc, orient, steps + 1))

        # Try Rotations
        new_orient = 1 - orient
        
        rotations_to_try = []
        if orient == 0: # horizontal -> vertical
            # Pivot 1: top-left end (r, c)
            rotations_to_try.append((r, c, r, c))
            # Pivot 2: other end (r, c+len-1)
            rotations_to_try.append((r - (length - 1), c + length - 1, r - (length - 1), c))
        else: # vertical -> horizontal
            # Pivot 1: top-left end (r, c)
            rotations_to_try.append((r, c, r, c))
            # Pivot 2: other end (r+len-1, c)
            rotations_to_try.append((r + length - 1, c - (length - 1), r, c - (length - 1)))

        for nr, nc, sr, sc in rotations_to_try:
            new_state = (nr, nc, new_orient)
            if new_state in visited:
                continue
            
            can_rotate = True
            if not (0 <= sr < M and 0 <= sc < N and sr + length - 1 < M and sc + length - 1 < N):
                can_rotate = False
            else:
                for i in range(length):
                    for j in range(length):
                        if grid[sr + i][sc + j] == 'B':
                            can_rotate = False
                            break
                    if not can_rotate:
                        break
            
            if can_rotate:
                visited.add(new_state)
                q.append((nr, nc, new_orient, steps + 1))

    print("Impossible")

run_solution()