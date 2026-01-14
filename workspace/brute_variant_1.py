import sys
from collections import deque

while True:
    line = sys.stdin.readline()
    if not line:
        break
    line = line.strip()
    if not line:
        continue
    
    try:
        M, N = map(int, line.split())
    except (ValueError, IndexError):
        continue

    grid = []
    try:
        for _ in range(M):
            grid_line = ""
            while not grid_line:
                grid_line = sys.stdin.readline()
                if not grid_line:
                    break
                grid_line = grid_line.strip()
            if not grid_line:
                break
            grid.append(grid_line.split())
    except (IOError, ValueError):
        break
    
    if len(grid) != M:
        continue

    source_coords = []
    target_coords = []
    for r in range(M):
        for c in range(N):
            if grid[r][c] == 'l':
                source_coords.append((r, c))
            elif grid[r][c] == 'L':
                target_coords.append((r, c))

    if not source_coords:
        if not target_coords:
            print(0)
        else:
            print("Impossible")
        continue

    length = len(source_coords)

    source_coords.sort()
    start_r, start_c = source_coords[0]
    start_orientation = 0
    if length > 1 and source_coords[1][0] != start_r:
        start_orientation = 1
    start_state = (start_r, start_c, start_orientation)

    target_coords.sort()
    target_r, target_c = target_coords[0]
    target_orientation = 0
    if length > 1 and target_coords[1][0] != target_r:
        target_orientation = 1
    target_state = (target_r, target_c, target_orientation)

    queue = deque([(start_state, 0)])
    visited = {start_state}

    found = False
    while queue:
        (r, c, orientation), dist = queue.popleft()

        if (r, c, orientation) == target_state:
            print(dist)
            found = True
            break

        # Moves
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            next_state = (nr, nc, orientation)
            if next_state in visited:
                continue
            
            is_valid = True
            if orientation == 0: # Horizontal
                if not (0 <= nr < M and 0 <= nc < N and nc + length - 1 < N):
                    is_valid = False
                else:
                    for i in range(length):
                        if grid[nr][nc + i] == 'B':
                            is_valid = False
                            break
            else: # Vertical
                if not (0 <= nr < M and 0 <= nc < N and nr + length - 1 < M):
                    is_valid = False
                else:
                    for i in range(length):
                        if grid[nr + i][nc] == 'B':
                            is_valid = False
                            break
            
            if is_valid:
                visited.add(next_state)
                queue.append((next_state, dist + 1))

        # Rotation
        can_rotate = True
        if not (0 <= r < M and 0 <= c < N and r + length - 1 < M and c + length - 1 < N):
            can_rotate = False
        else:
            for i in range(length):
                for j in range(length):
                    if grid[r + i][c + j] == 'B':
                        can_rotate = False
                        break
                if not can_rotate:
                    break
        
        if can_rotate:
            new_orientation = 1 - orientation
            next_state = (r, c, new_orientation)
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, dist + 1))

    if not found:
        print("Impossible")