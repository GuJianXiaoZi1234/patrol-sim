from pathplanning.bfs import find_path


def plan_patrol(start, points):
    segs = []
    cur = start
    for p in points:
        seg = find_path(cur, p)
        if seg is None:
            return None
        segs.append(seg)
        cur = p
    return segs
