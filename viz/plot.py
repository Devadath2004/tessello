import matplotlib.pyplot as plt

def plot_triangulation(points, triangles):
    fig, ax = plt.subplots()
    for tri in triangles:
        pts = [points[tri.a], points[tri.b], points[tri.c], points[tri.a]]
        xs = [p.x for p in pts]
        ys = [p.y for p in pts]
        ax.plot(xs, ys, 'b-')
    ax.set_aspect('equal')
    plt.show()
