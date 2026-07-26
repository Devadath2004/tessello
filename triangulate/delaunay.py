from geometry.primitives import Point, Triangle
from geometry.predicates import orientation, in_circumcircle
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
def find_bad_triangles(triangles, points, new_point):
    """
    triangles : list of objects (each storing 3 point *indices*)
    points : the master list of Point objects that the triangle's indices refer to
    new_point : the Point currently being inserted
    Returns : list of triangle objects whose circumcircle contains new point
    """
    bad =[]
    for tri in triangles:
        a = points[tri.a]
        b = points[tri.b]
        c = points[tri.c]
        if in_circumcircle(a,b,c,new_point):
            bad.append(tri)
    return bad
