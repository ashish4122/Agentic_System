import collections
import sys

def main():
    try:
        line = sys.stdin.readline()
        while line and not line.strip():
            line = sys.stdin.readline()
        if not line:
            return
        M, N = map(int, line.split())
    except (IOError, ValueError):
        return

    grid = []
    l_coords = []
    L_coords = []
    for r in range(M):
        row_line = sys.stdin.readline()
        while row_line and not row_line.strip():
            row_line = sys.stdin.readline()
        if not row_line:
            break
        row = row_line.split()
        grid.append(row)
        for c in range(N):
            if row[c] == 'l':
                l_coords.append((r, c))
            elif row[c] == 'L':
                L_coords.append((r, c))

    if not l_coords:
        if not L_coords:
            print(0)
        else:
            print("Impossible")
        return

    if not L_coords:
        print("Impossible")
        return

    l_coords.sort()
    start_r, start_c = l_coords[0]
    length = len(l_coords)
    start_orient = 0  # 0 for horizontal, 1 for vertical
    if length > 1 and l_coords[1][0] != start_r:
        start_orient = 1
    start_state = (start_r, start_c, start_orient)

    L_coords.sort()
    target_r, target_c = L_coords[0]
    target_orient = 0
    if length > 1 and L_coords[1][0] != target_r:
        target_orient = 1
    target_state = (target_r, target_c, target_orient)

    for r, c in l_coords:
        grid[r][c] = 'E'
    for r, c in L_coords:
        grid[r][c] = 'E'

    q = collections.deque([(start_state, 0)])
    visited = {start_state}

    def is_valid_position(r, c, orient):
        if orient == 0:  # horizontal
            if not (0 <= r < M and 0 <= c < N and c + length <= N):
                return False
            for i in range(length):
                if grid[r][c + i] == 'B':
                    return False
        else:  # vertical
            if not (0 <= r < M and 0 <= c < N and r + length <= M):
                return False
            for i in range(length):
                if grid[r + i][c] == 'B':
                    return False
        return True

    def is_valid_rotation_area(r, c):
        if not (0 <= r < M and 0 <= c < N and r + length <= M and c + length <= N):
            return False
        for i in range(length):
            for j in range(length):
                if grid[r + i][c + j] == 'B':
                    return False
        return True

    found = False
    while q:
        (r, c, orient), dist = q.popleft()

        if (r, c, orient) == target_state:
            print(dist)
            found = True
            break

        # 1. Translations
        dr = [-1, 1, 0, 0]
        dc = [0, 0, -1, 1]
        for i in range(4):
            nr, nc = r + dr[i], c + dc[i]
            next_state = (nr, nc, orient)
            if next_state not in visited and is_valid_position(nr, nc, orient):
                visited.add(next_state)
                q.append((next_state, dist + 1))

        # 2. Rotations
        new_orient = 1 - orient
        if orient == 0:  # horizontal -> vertical
            for i in range(length):  # pivot on horizontal cell i
                for j in range(length):  # pivot on vertical cell j
                    sq_r, sq_c = r - j, c
                    if is_valid_rotation_area(sq_r, sq_c):
                        new_r, new_c = r - j, c + i
                        next_state = (new_r, new_c, new_orient)
                        if next_state not in visited and is_valid_position(new_r, new_c, new_orient):
                            visited.add(next_state)
                            q.append((next_state, dist + 1))
        else:  # vertical -> horizontal
            for i in range(length):  # pivot on vertical cell i
                for j in range(length):  # pivot on horizontal cell j
                    sq_r, sq_c = r, c - j
                    if is_valid_rotation_area(sq_r, sq_c):
                        new_r, new_c = r + i, c - j
                        next_state = (new_r, new_c, new_orient)
                        if next_state not in visited and is_valid_position(new_r, new_c, new_orient):
                            visited.add(next_state)
                            q.append((next_state, dist + 1))

    if not found:
        print("Impossible")

if __name__ == "__main__":
    main()