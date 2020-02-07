# Recherche de solutions

Il n'y a **jamais d'intersection de segments entre deux polygones différents.**
Si un polygone A est contenu dans plusieurs autres polygones (B et C par exemple) alors il faut retourner le polygone (B ou C) le plus proche de A.

## Base
- Si un point d'un polygone A est dans un polygone B alors B contient A. Voir <http://alienryderflex.com/polygon/> pour réaliser ce test.

### Crossing-number
- Soit n le nombre de points du polygone, xi_poly et yi_poly les coordonnées du point i du polygone, x et y les coordonnées du point dont on cherche s'il appartient au polygone. Alors i va de 0 à n - 1 et j = n - 1.
si $$y_ipoly < ordo <= y_jpoly$$ ou $$y_jpoly < ordo <= y_ipoly$$
  si $$x_ipoly + \frac{(y - y_ipoly)(x_jpoly - x_ipoly)}{y_jpoly - y_ipoly} < x$$
    un noeud en plus


## Améliorations
- Si un polygone A contient un polygone B alors il contient tous les polygones contenus dans B.

- `__slots__` et `@property` dans polygon.py (gain négligeable devant ceux des slots de point.py et segment.py), point.py (gain timeit de 4ms) and segment.py (gain timeit de 10ms)

Depuis l'interpréteur :
```python
>> import timeit
>> timeit.timeit("from tycat import read_instance;polygones=read_instance('e3.poly'); sorted_poly = sorted(enumerate(polygones), key=lambda couple: couple[1].absolute_area, reverse=True)")
```
Dans le terminal :
```bash
python3 -m timeit -s "from tycat import read_instance" "polygones=read_instance('e3.poly'); sorted_poly = sorted(enumerate(polygones), key=lambda couple: couple[1].absolute_area, reverse=True)"
2000 loops, best of 5: 150 usec per loop
python3 -m timeit -s "from tycat import read_instance" "polygones=list(enumerate(read_instance('e3.poly'))); polygones.sort(key=lambda couple: couple[1].absolute_area, reverse=True)"
2000 loops, best of 5: 150 usec per loop
```

```bash
python3 -m timeit -r 5 -n 10 -s "from tycat import read_instance" "polygones=list(enumerate(read_instance('generated_from_examples.poly'))); polygones.sort(key=lambda couple: couple[1].absolute_area, reverse=True)"
5 loops, best of 5: 41 msec per loop
python3 -m timeit -r 5 -n 10 -s "from tycat import read_instance" "polygones=read_instance('generated_from_examples.poly'); sorted_poly = sorted(enumerate(polygones), key=lambda couple: couple[1].absolute_area, reverse=True)"
5 loops, best of 5: 41.7 msec per loop
```

L'ordre de l'enumerate et l'utilisation de sort plutôt que sorted influent peu les performances.
Une optimisation lru_cache n'apporte rien (pbl du hashage qui prend du temps).
L'utilisation de variables locales dans point_in_polygon.crossing_number fait perdre quelques secondes

Vérifier que le polygone (simple) est convexe : https://stackoverflow.com/questions/471962/how-do-i-efficiently-determine-if-a-polygon-is-convex-non-convex-or-complex/45372025#45372025
Méthode point inside polygone **convexe**:
 - créer les triangles entre deux sommets consécutifs et le point
 - la somme des aires doit être égale à celle du polygone
Voir https://www.geeksforgeeks.org/check-whether-given-point-lies-inside-rectangle-not/

Précalculation:
 - générer un rectangle (ou une boule) autour du polygone, si le point n'est pas dans le rectangle (la boule) (Méthode point inside polygone **convexe** car un rectangle est un polygone convexe / https://stackoverflow.com/questions/481144/equation-for-testing-if-a-point-is-inside-a-circle) alors celà ne sert à rien de tester toutes les arêtes avec le ray-crossing

## Notes
- Dans un cas quelconque :
  Effectuer des tests d'intersection de lignes pour chaque paire de lignes, chaque ligne appartenant à un polygone. Si aucune paire de lignes ne se croise et que l'un des points du polygone A se trouve à l'intérieur du polygone B, alors A est entièrement à l'intérieur de B. (en O(N*M) avec A polygone de N côtés et B polygone de M côtés)

  Ce qui précède fonctionne pour tout type de polygone. Si les polygones sont convexes, on peut ignorer les tests d'intersection de lignes et simplement **tester que tous les points de A sont à l'intérieur de B.**

  On peut accélérer les tests d'intersection de lignes à l'aide du *"sweep line algorithm"*.
- On a besoin de tester *seulement* si **un point de A sont à l'intérieur de B.**

- A consulter:
  - https://www.toptal.com/python/computational-geometry-in-python-from-theory-to-implementation
  - https://en.wikipedia.org/wiki/Point_in_polygon
