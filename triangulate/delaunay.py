from geometry.primitives import Point, Triangle

def super_triangle(points):
    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y=  max(p.y for p in points)

    dx = max_x - min_x
    dy = max_y - min_y
    
    delta = max(dx,dy)*10
    p1 = Point(min_x - delta, min_y - delta)
    p2 = Point(max_x + delta, min_y - delta)
    p3 = Point((min_x +max_x)/2, max_y+delta)

    return p1,p2,p3
