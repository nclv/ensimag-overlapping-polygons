# Projet d'algorithmque : inclusion de polygones

flags : DESSIN, 

Tous les fichiers du projet ne sont pas contenu dans l'archive. Les modifications apportées au module $geo$, certains affichages complémentaires, d'autres fichiers $.poly$, les jeux de tests, les programmes générateurs ainsi que l'ensemble des programmes développés lors de notre recherche de solution mais n'ayant pas aboutis se trouve sur le gitlab du projet.

## Analyse du problème

### Rappel du sujet
Il faut trouver les inclusions entre $n$ polygones simples ne s'intersectant pas entre eux et retourner une liste des inclusions, notée ici $results$.

La liste $results$ contient 
 - $-1$ à l'indice $i$ lorsque le $i$-ème polygone du fichier $.poly$ n'est inclu dans aucun autre polygone,
 - l'indice $j$ du polygone à l'indice $i$ lorsque le $i$-ème polygone du fichier $.poly$ est inclu dans le $j$-ème polygone du fichier $.poly$.

Que faire lorsqu'un polygone $i$ est inclus dans plusieurs autres polygones ? On chosit de récupérer dans $results$ le polygone le plus proche du polygone $i$, ie. le polygone d'aire la plus petite dans lequel se trouve le polygone $i$.

---

Tout d'abord quelques considérations...
 - Un polygone simple (ie. dont les arêtes ne s'intersectent pas entre elles) de $n$ sommets (et nécessairement $n$ arêtes) dans le plan est représenté par $2n$ réels,
 - Un ensemble de $n$ points nécessite $2n$ réels,
 - Un ensemble de $n$ segments nécessite $4n$ réels,
 - Un point ou un segment nécessite un stockage constant, ie. en $O(1)$.

Donc un polygone simple avec $n$ sommets nécessite un stockage linéaire, ie. en $O(n)$.

NB. Plutôt que de voir un polygone comme un ensemble de segments (comportants deux extrémités), on peut voir un polygone comme une ligne continue (ie. un ensemble de points) et ainsi réduire par deux le nombre de réels décrivant notre polygone.

On peut noter aussi que n'importe quelle opération entre deux objects de stockages constant prend un temps constant. On peut penser ici à des opérations comme un calcul de distance ou d'intersection.

Le temps d'exécution asymptotique d'un algorithme est toujours sensible par rapport à l'entrée (dépend entre autre de $n$).
On veut également que le temps d'exécution soit sensible par rapport à la sortie: si la sortie est volumineuse, c'est normal que l'algorithme soit plus long que si la sortie l'est peu, et dans ce cas, on souhaite un algorithme rapide.
La sortie est ici dépendante du nombre de polygones contenus dans le fichier $.poly$.

### Intersection d'une ligne avec $n$ segments

On peut se poser la question suivante : combien d'intersections nous nous attendons à avoir dans notre fichier de polygones ? Si on en attend $k$ et que $k = O(n)$ alors un algorithme en complexité temporelle $O(nlog(n))$ serait intéressant.

On choisit ici une ligne d'ordonnée fixe $y$ (facilitant les projections). On peut généraliser ce qui suit à une ligne quelconque.

Il est possible de faire une liste d'observations :
 - Une ligne d'ordonnée $y$ et un segment (deux points d'ordonnées $y0$ et $y1$) s'intersectent ssi. le point d'ordonnée $y$ se trouve sur le segment $[y0, y1]$. 

    On est alors ramené à un problème en 1D : étant donné un ensemble d'intervalles sur une droite réelle, trouver tous les intervalles contenant le point $y$ (ou alors éliminer tout ceux ne le contenant pas) (DESSIN).
 
 - Autre condition pour une ligne quelconque, il y a intersection ssi le produit des distances du sommet 0 avec la droite et du sommet 1 avec la droite est négatif.

 - Une ligne d'ordonnée $y$ et un segment (deux points d'ordonnées $y0$ et $y1$) peuvent s'intersecter ssi. la ligne et le segment sont adjacents dans une liste d'ordonnées triée ie. ce sont des voisins verticaux (DESSIN). Si c'est le cas, l'intersection ne peut avoir lieu qu'après que la ligne et le segment ne soient devenus des voisins verticaux.

    On est ramené à un algorithme de ligne de balayage faisant passer une ligne verticale de la gauche vers la droite ne gardant que les segments qui nous intéressent. Il faut pour celà définir le status et les évènements. Et faire attention à prendre en compte des cas spéciaux : deux extrémités de même abscisse par exemple.

    Pour la structure du status on peut utiliser un arbre binaire de recherche équilibré avec les segments qui coupent la ligne de balayage dans les feuilles. Pour stocker les évènements, on doit utiliser la même structure (distincte mais la même quoi... vous m'avez compris) parce que pendant le balayage on découvre des nouveaux évènements qui se réalisent plus tard.
    Donc sans détailler on a une complexité temporelle en $O(log(n))$ pour gérer un évènement, avec $2n$ (les points des segments) $+ k$ (le nombre de points d'intersections) soit $O(n + k)$ évènements au total.
    En résumé, remplir la structure d'évènements prend un temps $O(nlog(n))$, chacun des $O(n + k)$ évènement prend un temps $O(log(n))$ et donc, avec $k = O(n)$, l'algorithme est en $O(nlog(n))$.
    Cependant si $k$ est très grand, en pratique l'algorithme naïf en $O(n^2)$ est plus rapide.

On peut faire d'autres observations concernant les segments :
 - Pour un segment AB quelconque, une intersection est possible ssi. les intervalles $[y0, y1]$ et $[yA, yB]$ se chevauchent.

    Cette propriété n'est pas adaptée à une ligne car une ligne est infinie.


### Inclusions entre $n$ polygones

Nous avons eu ici différentes approches, avec des améliorations observées tout au long de ce projet.

Tout d'abord il est important d'initialiser chaque élément de la liste de polygone à $-1$. En effet, cela nous permet d'éviter de devoir construire la liste $results$ au fur et à mesure de nos comparaisons entre polygones (ie. $.append$ qui est coûteux à la longue...).

---

Une approche naïve serait de comparer chaque polygone avec les $(n - 1)$ autres polygones. Puis, en cas d'inclusions multiples, de choisir quel polygone renvoyer dans $results$.

Cette première étape est en $O(n^2)$ (sans compteur l'étape de détermination de l'inclusion qui se trouve dans cette double-boucle) donc à éviter. Le choix de quel polygone à renvoyer peut être optimisé si le stockage des polygones concernés est fait intelligemment.

---

Comment alors limiter le nombre de comparaisons (inutiles il s'entend) entre polygones ?

On ne veut pas réaliser les comparaisons inutiles lors d'inclusions multiples. Le critère de l'aire du polygone permet de choisir quelles comparaisons effectuer. A la fois lors d'inclusions multiples où l'on ne compare que les polygones qui sont voisins directs mais aussi plus globalement : on ne va pas tester qu'un polygone $poly_1$ d'aire supérieure à un polygone $poly_2$ se trouve dans le polygone $poly_2$.

Ainsi au lieu de $n^2$ tours de boucle, on en effectue $\frac{n(n - 1)}{2}$. Et si l'on se trouve avec $n$ polygones inclus les uns dans les autres (DESSIN), on n'effectue alors que $n - 1$ comparaisons.

---

Passons à l'inclusions en elle-même (ie. ce que l'on effectue dans notre boucle).

L'algorithme PIP (Point In Polygon) évoqué dans le sujet a une complexité en $O(m)$ où $m$ est le nombre de segments du polygone.

> Certaines propriétés des polygones permettent de simplifier des algorithmes. Il est ainsi possible de vérifier si un point se trouve dans un polygone **convexe** en $O(log(n))$ (Voir annexe a.1.).

> Ici cependant, nous avons aussi des polygones concaves. On a alors le choix entre utiliser un autre algorithme fonctionnant sur des polygones concaves ou alors découper notre polygone concave en polygones convexes (trigonalisation). Nous n'avons pas utilisé cette dernière approche.

La complexité temporelle est en $O(m.\frac{n(n - 1)}{2})$ dans le pire cas (zéro ou une unique inclusion par polygone). On peut chercher maintenant à réduire le nombre de passage par l'algorithme PIP.

La méthode des quadrants présente dans le module $geo$ peut nous y aider. En effet, si les *bounding boxes* des polygones ne s'intersectent pas, alors il n'y aura pas d'inclusions entre ces polygones.

Cela nous rajoute une étape de prétraitement en $O(n.m)$ lors de laquelle on calcule les *bounding boxes* de chaque polygone. Puis une comparaison en $O(1)$ :
```
b1.min_x < b2.max_x and b1.max_x > b2.min_x and b1.min_y < b2.max_y and b1.max_y > b2.min_y
```
S'il n'y a aucune intersection entre les *bounding boxes*, cela fait une complexité en $O(n.m + \frac{n(n - 1)}{2})$ (on n'appelle pas l'algorithme PIP). Si toutes les *bounding boxes* s'intersectent, on appelle à chaque tour l'algorithme PIP et la complexité temporelle est donc en $O(n.m + m\frac{n(n - 1)}{2})$. Dans le cas où on n'a que des inclusions multiples, les *bounding boxes* s'intersectent toutes entre elles et la complexité temporelle est en $O(n.m + m.(n - 1))$.

---

Revenons sur le cas des polygones convexes. Il est possible de vérifier qu'un polygone est convexe en $O(m)$ (indépendamment de s'il est simple ou non d'ailleurs). On peut effectuer cette opération sur les $n$ polygones avant d'entrer dans la boucle de comparaison (voir annexe a.2.), puis utiliser notre algorithme en $O(log(m))$ sur ces polygones.

On aurait alors une complexité en $O(n.m + log(m).\frac{n(n - 1)}{2})$ si tous nos polygones étaient convexes.

### Algorithmes PIP

Le principe de l'algorithme PIP évoqué dans le sujet est de boucler sur les segments du polygone $1$ et de compter les intersections avec une ligne passant par le point du polygone $2$.

On peut se poser deux questions :
 - comment choisir le point du polygone $2$?
 - comment choisir la ligne passant par ce point ?

Nous ferons le choix ici de ne compter que les intersections d'abscisses inférieures à l'abscisse du point choisi. Si ce nombre est impair, le point est dans le polygone.

De ce choix découle que l'on peut minimiser le nombre d'intersections calculées en prenant le point du polygone $2$ d'abscisse minimale, et ne considérer que les segments du polygone $1$ dont les points sont d'abscisses inférieures à cette abscisse maximale. Avec un tri des segments, on peut sortir directement de la boucle sur les segments dès que l'on rencontre un segment dont les deux points sont d'abscisses supérieures à l'abscisse maximale.

Pour éviter d'avoir à calculer d'autres points d'intersections inutiles, on utilise la seconde observation du paragraphe *Intersection d'une ligne avec $n$ segments*.
Elle se traduit par :
```python
ecart0, ecart1 = y0 - y, y1 - y
if ecart0 * ecart1 > 0 or ecart0 == ecart1 == 0:
   continue
```

Ce qui nous importe ne sont pas les intersections mais leur nombre. Il existe plusieurs méthodes de décompte.
La méthode que nous avons utilisé choisi de ne compter que les intersections "supérieures" ou "inférieures" selon le test utilisé.
```python
(y0 >= ordo > y1 or y1 >= ordo > y0)  # n'ajoute que les traits qui traversent la ligne y et ceux qui arrivent d'en bas avec une extrémité sur la ligne y
(y0 > ordo >= y1 or y1 > ordo >= y0)  # n'ajoute que les traits qui traversent la ligne y et ceux qui arrivent d'en haut avec une extrémité sur la ligne y
```
L'inconvénient de cette méthode est que l'on perd des points d'intersections et donc possiblement des polygones. Si l'on est intéressé par l'ensemble des polygones s'intersectant avec la ligne $y$ on est obligé d'effectuer les deux tests, calculant ainsi des points d'intersections en double.

On peut penser à une autre méthode de décompte, nécessitant de connaître l'orientation entre deux segments successifs. Il est alors nécessaire de calculer celle-ci avant d'effectuer le tri des segments (ou alors de ne pas trier les segments). On raisonne ensuite par énumération des cas : traversée de haut en bas, traversée de bas en haut, segment confondu avec la ligne (deux sous-cas ici, selon que les segments précédent et suivant aillent du même côté ou non de la ligne), coin supérieur et coin inférieur.

On peut maintenant calculer l'abscisse du point d'intersection et tester si elle est plus petite que celle du point du polygone $2$. Ci-dessous la formule déterminant l'abscisse du point d'intersection :
```python
interx = x1 + (ordo - y1) / (y0 - y1) * (x0 - x1)
```

---

La méthode précédente se prête aux erreurs numériques (et possiblement une division par 0 si l'on change les conditions du $if$) lors du calcul de l'intersection. Il est possible de ne pas réaliser ce calcul.

On peut utiliser un simple compteur auquel l'on ajoute $1$ lorsque que l'on coupe la ligne vers le haut et un $-1$ si on la coupe vers le bas. Il faut aussi prendre en compte si le point est placé à gauche ou à droite du segment orienté et faire un choix : ne compter que les segments situés à gauche du point ou seulement ceux situés à sa droite.

Déterminer la position relative d'un point par rapport à une ligne peut se faire par un simple calcul d'aire signé.
```python
(x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
```
Si cette aire est positive (resp. négative), le point 2 à gauche (resp. droite) du segment orienté $[p0, p1]$.


TODO: 
- Le tracé d'une ligne
- L'importance du choix de la division lsq diviser pour régner

Liste des fichiers pour les tests de correction :
 - (8/12)_polygons_multiples_inclusions, 1_square, 4_triangles_multiples_inclusions, 19_polygons_some_overlapping, 14_polygons_limit_cases, 3_polygons_limit_case
 - 8_polygons_1round_shape
 - 17_squares_overlapping
 - 10x10, 10x20c10000, e2

Liste des fichiers pour les tests de performance :
 - e2, 10x10
 - 2_circular_shape
 - 147_polygons_without_overlap
 - 25_polygons_around_1complex_shape
 - overlapping_square_4 / 100 / 1000 / ...
 - upper_and_left_duplication_2 / 64 / 256 / ...

Liste des algorithmes :
 - Avec crossing_number, crossing_number_v2, crossing_number_v3, crossing_number_v3_sec, crossing_number_v3_segments, winding_number, crossing_number_v5
 - trouve_inclusions, trouve_inclusions_sorted, trouve_inclusions_bis, trouve_inclusions_general (avec et sans test des quadrants)

## Générateurs d'entrées

S'il est important de distinguer le comportement asymptotique du temps d'exécution réelle de notre algorithme, c'est en partie parce que les paramètres en entrée sont déterminants.

Nous n'avons pas souhaité développer des algorithmes de génération d'un ensemble quelconque de polygones.
Nous avons cherché les cas qui pourraient poser problème à nos algorithmes et programmé des duplicateurs étant capables de les créer.

Nous pouvons actuellement générer :
 - l'inclusion d'un très grand nombre de polygones,
 - la duplication d'un ensemble de polygones selon l'axe des ordonnées, l'axe des abscisses ou les deux axes,

## Mesures temporelles

On cherche ici à minimiser les erreurs systématique et aléatoire. Pour plus d'information sur la méthode utilisée consulter ce [lien](https://github.com/NicovincX2/python-tools/blob/master/measuring-code-execution-time.md).

## Annexes
a.1.
- Une approche est de trianguler le polygone en traçant les arêtes d'un sommet à tous les autres, trouver l'angle où se trouve le point en utilisant une recherche dichotomique et ensuite vérifier si le point est dans le triangle ou non.
- On peut penser à une autre approche. Si le point est en dessous (ou à gauche sur la même droite horizontale) que le sommet inférieur (ie. le sommet de plus petite ordonnée) gauche, le sommet est hors du polygone. On a le même raisonnement pour le sommet supérieur droit. On connecte ces deux sommets. Si le point est sur ce segment, il est soit sur la limite du polygone (confondu avec les extrémités du segment ou sinon ce segment est une arête du polygone), soit à l'intérieur du polygone. Si le point est à droite (ou à gauche de manière analogue), nous devons vérifier s'il se trouve à gauche de la chaîne droite construite par l'algorithme du calcul de l'enveloppe convexe (DESSIN). L'arrête correspondante est trouvée en utilisant la recherche dichotomique, en comparant les points lexicographiquement.

a.2.

*(Quick and)* **Dirty** : `[all((a - c) * (d - f) <= (b - d) * (c - e) for (a, b), (c, d), (e, f) in zip(p[-2:] + p, [p[-1]] + p + [p[0]], p))::2]` où $p$ est une liste de points.

Voir [ce post](https://stackoverflow.com/a/1881201) pour plus d'informations.