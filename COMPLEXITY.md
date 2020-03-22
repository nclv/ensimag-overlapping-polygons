A simple polygon in the plane can be represented using 2n reals if it has n vertices (and necessarily, n edges)
A set of n points requires 2n reals 
A set of n line segments requires 4n reals 
A point, line, circle,...requires O(1), or constant, storage.
A simple polygon with n vertices requires O(n), or linear, storage

Any computation (distance, intersection) on two objects of O(1) description size takes O(1) time

https://codeforces.com/blog/entry/48868

Observation:Two line segments can only intersect if their y-spans have an overlap
So, how about only testing pairs of line segments that intersect in they-projection?
1-D problem:  Given a set of intervalson the real line, find all partly overlapping pairs (p34)
Refined observation: Two line segments can only intersect if their y-spans have an overlap, 
and they are adjacent in the x-order at that y-coordinate (they are horizontal neighbors)
Two line segments si and sj can only intersect after (= below) they have become horizontal neighbors
https://www.cise.ufl.edu/~sitharam/COURSES/CG/kreveldintrolinesegment.pdf

Comment sélectionner le point à partir duquel tracer la droite y ?
 - on prend celui avec l'abscisse la plus petite (et on compte le nombre d'intersections à gauche)
 - sinon on prend le max des abscisses des points sur la droite y (et on compte le combre d'intersections à gauche)
