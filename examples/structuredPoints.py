from geometry.primitives import Point

def squarePoints(n):
    pts = []
    for i in range(n):
        for j in range(n):
            x = i
            y = j
            pts.append(Point(x, y))
    return pts

