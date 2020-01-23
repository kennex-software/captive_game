#kennex

def scale_points_list(points, xd, yd):
    """This function is to scale a list of points based by specific X and Y values.
    This was created because in pygame you can click points for an object to draw, but you need to put it on a surface
        and when you go to draw it, you need to change up the values of the list.

    points = points list
    xd = Change in X Value (x delta)
    yd = Change in Y Value (y delta)

    Changed values can be printed or returned.
    """

    for index, point in enumerate(points):
        newx = xd + int(point[0])
        newy = yd + int(point[1])
        new_point = (newx, newy)
        points[index] = tuple(new_point)

    return points

points_list = [(34, 3), (40, 5), (40, 25), (69, 68), (1, 53), (40, 25)]

scale_points_list(points_list, 100, 250)

print(points_list)