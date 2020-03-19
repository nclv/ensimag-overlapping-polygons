#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
polygones_generator.py : générateur de polygones
"""


from random import seed, random
from geo.polygon import Polygon
from geo.segment import Segment
from geo.point import Point


def random_coordinates_generator(nombre):
    seed(1)
    for _ in range(nombre):
        yield [random(), random()]

def random_points_generator(nombre):
    return map(Point, random_coordinates_generator(NOMBRE))

def main():
    NOMBRE = 100
    segments = [] # contient des listes de deux points
    for new_pointa, new_pointb in zip(random_points_generator(NOMBRE), random_points_generator(NOMBRE)):
        new_segment = [new_pointa, new_pointb]
        for indice in range(len(segments)):
            pointc, pointd = segments[i]
            if Segment(new_segment).intersect(Segment([pointc, pointd])):
                # si intersection, on swap les points
                new_segment = [new_pointa, pointc]
                # segments[indice] devient un nouveau segment
                # on doit vérifier qu'il ne s'intersecte pas avec d'autres
                segments[indice] = [new_pointb, pointd]
        segments.append(new_segment) # on ajoute le segment dans tous les cas

def old_main():
    """main function"""
    nombre_de_points = 100
    coordonnees_des_points = 10
    limit = random.randrange(2, nombre_de_points)

    polygones = [Polygon([Point([1, 2]), Point([2, 4]), Point([-1, 2])])]
    for _ in range(3):
        points = [
            Point(
                [
                    random.randrange(coordonnees_des_points),
                    random.randrange(coordonnees_des_points),
                ]
            )
        ]
        segments = []
        for _ in range(limit):
            # on ajoute le polygone si aucun de ses segments ne s'intersecte avec un segment déjà existant
            point = Point(
                [
                    random.randrange(coordonnees_des_points),
                    random.randrange(coordonnees_des_points),
                ]
            )
            print(points, segments)
            failed = is_failed(polygones, segments, points, point)

            if not failed:
                segment = Segment([points[-1], point])
                if point not in points:
                    points.append(point)
                if segment not in segments:
                    segments.append(segment)

        if len(points) > 2:
            polygon = Polygon(points)
            if polygon.area() != 0:
                polygones.append(polygon)

    with open("generated.poly", "w") as file:
        for indice, polygone in enumerate(polygones):
            for point in polygone.points:
                file.write(f"{indice} {point.coordinates[0]} {point.coordinates[1]}\n")


def is_failed(polygones, segments, points, point):
    for polygon in polygones:
        for segment in list(polygon.segments()) + segments:
            if segment.intersect(Segment([points[-1], point])):
                return True

def generatePolygon( ctrX, ctrY, aveRadius, irregularity, spikeyness, numVerts ) :
    '''Start with the centre of the polygon at ctrX, ctrY,
    then creates the polygon by sampling points on a circle around the centre.
    Randon noise is added by varying the angular spacing between sequential points,
    and by varying the radial distance of each point from the centre.

    https://github.com/the-mikedavis/randompolygons

    Params:
    ctrX, ctrY - coordinates of the "centre" of the polygon
    aveRadius - in px, the average radius of this polygon, this roughly controls how large the polygon is, really only useful for order of magnitude.
    irregularity - [0,1] indicating how much variance there is in the angular spacing of vertices. [0,1] will map to [0, 2pi/numberOfVerts]
    spikeyness - [0,1] indicating how much variance there is in each vertex from the circle of radius aveRadius. [0,1] will map to [0, aveRadius]
    numVerts - self-explanatory

    Returns a list of vertices, in CCW order.
    '''
    import math, random

    irregularity = clip( irregularity, 0,1 ) * 2*math.pi / numVerts
    spikeyness = clip( spikeyness, 0,1 ) * aveRadius

    # generate n angle steps
    angleSteps = []
    lower = (2*math.pi / numVerts) - irregularity
    upper = (2*math.pi / numVerts) + irregularity
    sum = 0
    for i in range(numVerts):
        tmp = random.uniform(lower, upper)
        angleSteps.append( tmp )
        sum = sum + tmp

    # normalize the steps so that point 0 and point n+1 are the same
    k = sum / (2*math.pi)
    for i in range(numVerts):
        angleSteps[i] = angleSteps[i] / k

    # now generate the points
    points = []
    angle = random.uniform(0, 2*math.pi)
    for i in range(numVerts):
        r_i = clip( random.gauss(aveRadius, spikeyness), 0, 2*aveRadius )
        x = ctrX + r_i*math.cos(angle)
        y = ctrY + r_i*math.sin(angle)
        points.append( (int(x),int(y)) )

        angle = angle + angleSteps[i]

    return points

def clip(x, min, max):
    if( min > max ):
        return x
    elif( x < min ):
        return min
    elif( x > max ):
        return max
    else:
        return x

if __name__ == "__main__":
    # old_main()
    # assert (
    #     Segment([Point([1, 1]), Point([-1, -1])]).intersect(
    #         Segment([Point([-1, 1]), Point([1, -1])])
    #     )
    #     is True
    # )
    verts = generatePolygon( ctrX=250, ctrY=250, aveRadius=100, irregularity=0.7, spikeyness=0.8, numVerts=16)
    # polygon = Polygon(list(map(Point, verts)))
    from PIL import Image, ImageDraw
    black = (0,0,0)
    white=(255,255,255)
    im = Image.new('RGB', (500, 500), white)
    imPxAccess = im.load()
    draw = ImageDraw.Draw(im)
    tupVerts = list(map(tuple, verts))

    # either use .polygon(), if you want to fill the area with a solid colour
    draw.polygon(tupVerts, outline=black,fill=white )

    # or .line() if you want to control the line thickness, or use both methods together!
    draw.line(tupVerts+[tupVerts[0]], width=2, fill=black )

    im.show()
