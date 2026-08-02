from geometry.primitives import Point, Triangle
from geometry.predicates import orientation, in_circumcircle
from viz.plot import plot_triangulation
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
def make_triangle(i1,i2,i3,points):
    """ 
    construct a Triangle from the three point indices, guaranteeing counterclockwise winding regardless of input order.
    """
    a,b,c = points[i1],points[i2],points[i3]
    if orientation(a,b,c) == -1:
        i2,i3=i3,i2
    return Triangle(i1,i2,i3)
def find_boundary_edges(bad_triangles):
    """
    given a list of bad triangle objects, return the edges that appear only once, these will be the boundary edges. 
    The edges are returned as tuples of point indices
    """
    edge_count = {}
    for tri in bad_triangles:
        edges = [(tri.a,tri.b),(tri.a,tri.c),(tri.b,tri.c)]
        for i,j in edges:
            key = (min(i,j),max(i,j))
            edge_count[key] = edge_count.get(key,0)+1
    boundary =[edge for edge, count in edge_count.items() if count == 1]
    return boundary
def bowyer_watson(input_points):
    points = list(input_points)
    s1,s2,s3= super_triangle(points)
    points.append(s1)
    points.append(s2)
    points.append(s3)
    s1_idx,s2_idx,s3_idx = len(points) - 3, len(points) - 2,len(points) -1
    triangles = [make_triangle(s1_idx,s2_idx,s3_idx,points)]
    for point_idx in range(len(points)):
        p = points[point_idx]
        bad = find_bad_triangles(triangles,points,p)
        for tri in bad:
            triangles.remove(tri)
        boundary = find_boundary_edges(bad)
        for i,j in boundary:
            new_tri = make_triangle(i,j,point_idx,points)
            triangles.append(new_tri)
    final=[]
    for tri in triangles:
        if s1_idx in (tri.a,tri.b,tri.c):
            continue
        if s2_idx in (tri.a,tri.b,tri.c):
            continue
        if s3_idx in (tri.a,tri.b,tri.c):
            continue
        final.append(tri)
    return(points,final)

def bowyer_watson_live(input_points):
    points = list(input_points)
    s1, s2, s3 = super_triangle(points)
    points.append(s1)
    points.append(s2)
    points.append(s3)
    s1_idx, s2_idx, s3_idx = len(points) - 3, len(points) - 2, len(points) - 1

    triangles = [make_triangle(s1_idx, s2_idx, s3_idx, points)]

    for point_idx in range(len(input_points)):
        p = points[point_idx]

        bad = find_bad_triangles(triangles, points, p)
        for tri in bad:
            triangles.remove(tri)

        boundary = find_boundary_edges(bad)

        for (i, j) in boundary:
            new_tri = make_triangle(i, j, point_idx, points)
            triangles.append(new_tri)

        plot_triangulation(points, triangles)  # <-- the only real addition

    final = []
    for tri in triangles:
        if s1_idx in (tri.a, tri.b, tri.c):
            continue
        if s2_idx in (tri.a, tri.b, tri.c):
            continue
        if s3_idx in (tri.a, tri.b, tri.c):
            continue
        final.append(tri)

    return points, final   
