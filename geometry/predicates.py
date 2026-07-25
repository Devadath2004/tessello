def orientation(a,b,c):
    cross = (b.x-a.x) * (c.y-a.y) - (b.y-a.y) * (c.x-a.x)
    if cross > 0:
        return 1
    elif cross < 0:
        return -1
    else:
        return 0
