#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
utils.py : //
"""
import math

# voir https://docs.scipy.org/doc/numpy/reference/generated/almostEqual.html
def almostEqual(x, y, rtol=1.0e-12, atol=1.0e-12):
    return abs(x - y) <= (atol + rtol * abs(y))


def clip_line_by_polygon(line, polygon,
                         closed=True,
                         check_input=True):
    """Clip line segments by polygon
    Input
       line: Sequence of line nodes: [[x0, y0], [x1, y1], ...] or
             the equivalent Nx2 numpy array
       polygon: list of vertices of polygon or the corresponding numpy array
       closed: (optional) determine whether points on boundary should be
       regarded as belonging to the polygon (closed = True)
       or not (closed = False) - False is not recommended here
       check_input: Allows faster execution if set to False
    Outputs
       inside_lines: Clipped lines that are inside polygon
       outside_lines: Clipped lines that are outside polygon
       Both outputs take the form of lists of Nx2 line arrays
    Example:
        U = [[0,0], [1,0], [1,1], [0,1]]  # Unit square
        # Simple horizontal fully intersecting line
        line = [[-1, 0.5], [2, 0.5]]
        inside_line_segments, outside_line_segments = \
            clip_line_by_polygon(line, polygon)
        print numpy.allclose(inside_line_segments,
                              [[[0, 0.5], [1, 0.5]]])
        print numpy.allclose(outside_line_segments,
                              [[[-1, 0.5], [0, 0.5]],
                               [[1, 0.5], [2, 0.5]]])
    Remarks:
       The assumptions listed in separate_points_by_polygon apply
       Output line segments are listed as separate lines i.e. not joined
    """

    # Get polygon extents to quickly rule out points that
    # are outside its bounding box
    points_x, points_y = zip(*[point for point in polygon])
    minpx = min(points_x)
    maxpx = max(points_x)
    minpy = min(points_y)
    maxpy = max(points_y)

    N = len(polygon) # Number of vertices in polygon
    M = len(line)  # Number of segments

    # Algorithm
    #
    # 1: Find all intersection points between line segments and polygon edges
    # 2: For each line segment
    #    * Calculate distance from first end point to each intersection point
    #    * Sort intersection points by distance
    #    * Cut segment into multiple segments
    # 3: For each new line segment
    #    * Calculate its midpoint
    #    * Determine if it is inside or outside clipping polygon

    # FIXME (Ole): Vectorise

    # Loop through line segments
    for k in range(M - 1):
        intersections = 0
        p0 = line[k]
        p1 = line[k + 1]
        segment = [p0, p1]

        # Skip segments where both end points are outside polygon bounding box
        # and which don't intersect the bounding box
        segment_is_outside_bbox = True
        for p in [p0, p1]:
            x = p[0]
            y = p[1]
            if not (x > maxpx or x < minpx or y > maxpy or y < minpy):
                #  This end point is inside polygon bounding box
                segment_is_outside_bbox = False
                break

        # Does segment intersect polygon bounding box?
        corners = [[minpx, minpy], [maxpx, minpy], [maxpx, maxpy], [minpx, maxpy]]
        for i in range(3):
            edge = [corners[i], corners[i + 1]]
            status, value = intersection(segment, edge)
            if value is not None:
                # Segment intersects polygon bounding box
                segment_is_outside_bbox = False
                break

        # Separate segments that are inside from those outside
        if not segment_is_outside_bbox:
            # Intersect segment with all polygon edges
            # and decide for each sub-segment
            for i in range(N):
                # Loop through polygon edges
                j = (i + 1) % N
                edge = [polygon[i], polygon[j]]

                status, value = intersection(segment, edge)
                if status == 2:
                    # Collinear overlapping lines found
                    # value = (value[0] + value[1]) / 2
                    pass

                if value is not None:
                    # Record intersection point found
                    intersections += 1
                else:
                    pass

    return intersections


def point_on_line(point, line, rtol=1.0e-5, atol=1.0e-8):
    """Determine if a point is on a line segment
    Input
        points: Coordinates of either
                * one point given by sequence [x, y]
        line: Endpoint coordinates [[x0, y0], [x1, y1]] or
              the equivalent 2x2 numeric array with each row corresponding
              to a point.
        rtol: Relative error for how close a point must be to be accepted
        atol: Absolute error for how close a point must be to be accepted
    Output
        True or False
    Notes
    Line can be degenerate and function still works to discern coinciding
    points from non-coinciding.
    Tolerances rtol and atol are used with almostEqual()
    """

    x, y = point
    x0, y0 = line[0]
    x1, y1 = line[1]

    # Vector from beginning of line to point
    a0 = x - x0
    a1 = y - y0

    # It's normal vector
    a_normal0 = a1
    a_normal1 = -a0

    # Vector parallel to line
    b0 = x1 - x0
    b1 = y1 - y0

    # Dot product
    nominator = abs(a_normal0 * b0 + a_normal1 * b1)
    denominator = b0 * b0 + b1 * b1

    # Determine if point is parallel to line up to a tolerance
    is_parallel = nominator <= atol + rtol * denominator

    # Determine for points parallel to line if they are within end points
    a0p = a0 if is_parallel else 0
    a1p = a1 if is_parallel else 0

    len_a = math.sqrt(a0p * a0p + a1p * a1p)
    len_b = math.sqrt(b0 * b0 + b1 * b1)
    cross = a0p * b0 + a1p * b1

    # Result is True only if a0 * b0 + a1 * b1 >= 0 and len_a <= len_b
    result = (cross >= 0) * (len_a <= len_b)
    return result

def intersection(line0, line1, rtol=1.0e-12, atol=1.0e-12):
    """Returns intersecting point between two line segments.
    However, if parallel lines coincide partly (i.e. share a common segment),
    the line segment where lines coincide is returned
    Inputs:
        line0, line1: Each defined by two end points as in:
                      [[x0, y0], [x1, y1]]
                      A line can also be a 2x2 numpy array with each row
                      corresponding to a point.
        rtol, atol: Tolerances passed onto almostEqual
    Output:
        status, value - where status and value is interpreted as follows:
        status == 0: no intersection, value set to None.
        status == 1: intersection point found and returned in value as [x,y].
        status == 2: Collinear overlapping lines found.
                     Value takes the form [[x0,y0], [x1,y1]] which is the
                     segment common to both lines.
        status == 3: Collinear non-overlapping lines. Value set to None.
        status == 4: Lines are parallel. Value set to None.
    """
    # line0 est une ligne horizontal : x0 valeur de x minimale et y0 = y1
    x0, y0 = line0[0]
    x1, y1 = line0[1]

    x2, y2 = line1[0]
    x3, y3 = line1[1]

    # denom = (y3 - y2) * (x1 - x0) - (x3 - x2) * (y1 - y0)
    # u0 = (x3 - x2) * (y0 - y2) - (y3 - y2) * (x0 - x2)
    # u1 = (x2 - x0) * (y1 - y0) - (y2 - y0) * (x1 - x0)
    denom = (y3 - y2) * (x1 - x0) # sign(y3 - y2) * infinie car x1 infini
    u0 = (x3 - x2) * (y0 - y2) - (y3 - y2) * (x0 - x2)
    u1 = - (y2 - y0) * (x1 - x0) # -sign(y2 - y0) * infini car x1 infini

    if almostEqual(denom, 0.0, rtol=rtol, atol=atol):
        # Lines are parallel - check if they are collinear
        if almostEqual(u0, 0.0, rtol=rtol, atol=atol) and almostEqual(u1, 0.0, rtol=rtol, atol=atol):
            print("colinear")
            # We now know that the lines are collinear
            state = (point_on_line([x0, y0], line1, rtol=rtol, atol=atol),
                     point_on_line([x1, y1], line1, rtol=rtol, atol=atol),
                     point_on_line([x2, y2], line0, rtol=rtol, atol=atol),
                     point_on_line([x3, y3], line0, rtol=rtol, atol=atol))

            return collinearmap[state]([x0, y0], [x1, y1],
                                       [x2, y2], [x3, y3])
        else:
            # Lines are parallel but aren't collinear
            return 4, None  # FIXME (Ole): Add distance here instead of None
    else:
        # Lines are not parallel, check if they intersect
        u0 = u0 / denom
        u1 = u1 / denom

        x = x0 + u0 * (x1 - x0) # u0 * infinie
        y = y0 # + u0 * (y1 - y0)

        # Sanity check - can be removed to speed up if needed
        if not almostEqual(x, x2 + u1 * (x3 - x2), rtol=rtol, atol=atol):
            raise Exception
        if not almostEqual(y, y2 + u1 * (y3 - y2), rtol=rtol, atol=atol):
            raise Exception

        # Check if point found lies within given line segments
        if 0.0 <= u0 <= 1.0 and 0.0 <= u1 <= 1.0:
            # We have intersection
            return 1, [x, y]
        else:
            print(u0, u1)
            # No intersection
            return 0, None


# Result functions used in intersection() below for possible states
# of collinear lines
# (p0,p1) defines line 0, (p2,p3) defines line 1.

def lines_dont_coincide(p0, p1, p2, p3):
    print(lines_dont_coincide)
    return 3, None


def lines_0_fully_included_in_1(p0, p1, p2, p3):
    print(lines_0_fully_included_in_1)
    return 2, [p0, p1]


def lines_1_fully_included_in_0(p0, p1, p2, p3):
    print(lines_1_fully_included_in_0)
    return 2, [p2, p3]


def lines_overlap_same_direction(p0, p1, p2, p3):
    print(lines_overlap_same_direction)
    return 2, [p0, p3]


def lines_overlap_same_direction2(p0, p1, p2, p3):
    print(lines_overlap_same_direction2)
    return 2, [p2, p1]


def lines_overlap_opposite_direction(p0, p1, p2, p3):
    print(lines_overlap_opposite_direction)
    return 2, [p0, p2]


def lines_overlap_opposite_direction2(p0, p1, p2, p3):
    print(lines_overlap_opposite_direction2)
    return 2, [p3, p1]


# This function called when an impossible state is found
def lines_error(p1, p2, p3, p4):
    msg = ('Impossible state: p1=%s, p2=%s, p3=%s, p4=%s'
           % (str(p1), str(p2), str(p3), str(p4)))
    raise RuntimeError(msg)

# Mapping to possible states for line intersection
#
#                 0s1    0e1    1s0    1e0   # line 0 starts on 1, 0 ends 1,
#                                                   1 starts 0, 1 ends 0
collinearmap = {(False, False, False, False): lines_dont_coincide,
                (False, False, False, True): lines_error,
                (False, False, True, False): lines_error,
                (False, False, True, True): lines_1_fully_included_in_0,
                (False, True, False, False): lines_error,
                (False, True, False, True): lines_overlap_opposite_direction2,
                (False, True, True, False): lines_overlap_same_direction2,
                (False, True, True, True): lines_1_fully_included_in_0,
                (True, False, False, False): lines_error,
                (True, False, False, True): lines_overlap_same_direction,
                (True, False, True, False): lines_overlap_opposite_direction,
                (True, False, True, True): lines_1_fully_included_in_0,
                (True, True, False, False): lines_0_fully_included_in_1,
                (True, True, False, True): lines_0_fully_included_in_1,
                (True, True, True, False): lines_0_fully_included_in_1,
                (True, True, True, True): lines_0_fully_included_in_1}
