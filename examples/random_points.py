import random
from geometry.primitives import Point

def random_points(n,x_min = 0,y_min=0,x_max=10,y_max=10):
    points=[]
    for _ in range(n):
        x = random.uniform(x_min,x_max)
        y = random.uniform(y_min,y_max)
        points.append(Point(x,y))
    return points
