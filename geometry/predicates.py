def orientation(a,b,c):
    cross = (b.x-a.x) * (c.y-a.y) - (b.y-a.y) * (c.x-a.x)
    if cross > 0:
        return 1
    elif cross < 0:
        return -1
    else:
        return 0
def in_circumcircle(a,b,c,d):
    ax, ay = a.x - d.x, a.y - d.y
    bx, by = b.x - d.x, b.y - d.y
    cx, cy = c.x - d.x, c.y - d.y
    ax2ay2 = ax*ax +ay*ay
    bx2by2 = bx*bx +by*by
    cx2cy2 = cx*cx +cy*cy

    det = (ax * (by * cx2cy2 - bx2by2 * cy)
           - ay * (bx * cx2cy2 - bx2by2 * cx)
           + ax2ay2 * (bx * cy - by * cx))

    return det > 0

