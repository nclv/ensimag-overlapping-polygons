# Projet d'algorithmque : inclusion de polygones

flags : DESSIN, 

Tous les fichiers du projet ne sont pas contenu dans l'archive. Les modifications apportées au module $geo$, certains affichages complémentaires, d'autres fichiers $.poly$, les jeux de tests, les programmes générateurs ainsi que l'ensemble des programmes développés lors de notre recherche de solution mais n'ayant pas aboutis se trouve sur le gitlab du projet.

Une liste des algorithmes et fichiers de tests est présente en annexe $a.3.$.

## Analyse du problème

### Rappel du sujet
Il faut trouver les inclusions entre $n$ polygones simples ne s'intersectant pas entre eux et retourner une liste des inclusions, notée ici $results$.

La liste $results$ contient 
 - $-1$ à l'indice $i$ lorsque le $i$-ème polygone du fichier $.poly$ n'est inclu dans aucun autre polygone,
 - l'indice $j$ du polygone à l'indice $i$ lorsque le $i$-ème polygone du fichier $.poly$ est inclu dans le $j$-ème polygone du fichier $.poly$.

Que faire lorsqu'un polygone $i$ est inclu dans plusieurs autres polygones ? On choisit de récupérer dans $results$ le polygone le plus proche du polygone $i$, ie. le polygone d'aire la plus petite dans lequel se trouve le polygone $i$.

---

Tout d'abord quelques considérations...
 - Un polygone simple (ie. dont les arêtes ne s'intersectent pas entre elles) de $n$ sommets (et nécessairement $n$ arêtes) dans le plan est représenté par $2n$ réels,
 - Un ensemble de $n$ points nécessite $2n$ réels,
 - Un ensemble de $n$ segments nécessite $4n$ réels,
 - Un point ou un segment nécessite un stockage constant, ie. en $O(1)$.

Donc un polygone simple avec $n$ sommets nécessite un stockage linéaire, ie. en $O(n)$.

NB. Plutôt que de voir un polygone comme un ensemble de segments (comportants deux extrémités), on peut voir un polygone comme une ligne continue (ie. un ensemble de points) et ainsi réduire par deux le nombre de réels décrivant notre polygone.

On peut noter aussi que n'importe quelle opération entre deux objets de stockage constant prend un temps constant. On peut penser ici à des opérations comme un calcul de distance ou d'intersection.

Le temps d'exécution asymptotique d'un algorithme est toujours sensible par rapport à l'entrée.
On veut également que le temps d'exécution soit sensible par rapport à la sortie: si la sortie est volumineuse, c'est normal que l'algorithme soit plus long que si la sortie l'est peu, et dans ce cas, on souhaite un algorithme rapide.
La sortie est ici dépendante du nombre de polygones contenus dans le fichier $.poly$.

### Intersection d'une ligne avec $n$ segments

On peut se poser la question suivante : combien d'intersections nous nous attendons à avoir dans notre fichier de polygones ? Si on en attend $k$ et que $k = O(n)$ alors un algorithme en complexité temporelle $O(nlog(n))$ serait intéressant.

On choisit ici une ligne d'ordonnée fixe $y$ (facilitant les projections).

Il est possible de faire une liste d'observations :
 - Une ligne d'ordonnée $y$ et un segment (deux points d'ordonnées $y0$ et $y1$) s'intersectent ssi. le point d'ordonnée $y$ se trouve sur le segment $[y0, y1]$ (DESSIN). 

    On est alors ramené à un problème en 1D : étant donné un ensemble d'intervalles sur une droite réelle, trouver tous les intervalles contenant le point $y$ (ou alors éliminer tout ceux ne le contenant pas) (DESSIN).
 
 - Autre condition (fonctionnant aussi pour une ligne quelconque): il y a intersection ssi le produit des distances du sommet 0 avec la droite et du sommet 1 avec la droite est négatif.

 - Une ligne d'ordonnée $y$ et un segment (deux points d'ordonnées $y0$ et $y1$) peuvent s'intersecter ssi. la ligne et le segment sont adjacents dans une liste d'ordonnées triée ie. ce sont des voisins verticaux (DESSIN). Si c'est le cas, l'intersection ne peut avoir lieu qu'après que la ligne et le segment ne soient devenus des voisins verticaux.

    On est ramené à un algorithme de ligne de balayage faisant passer une ligne verticale de la gauche vers la droite ne gardant que les segments qui nous intéressent. Il faut pour cela définir le status et les évènements. Et faire attention aux cas spéciaux lors du décompte des intersections: deux extrémités de même abscisse par exemple.

    Pour la structure du status on peut utiliser un arbre binaire de recherche équilibré avec les segments qui coupent la ligne de balayage dans les feuilles. Pour stocker les évènements, on doit utiliser une structure identique parce que pendant le balayage on découvre des nouveaux évènements qui se réalisent plus tard.
    Donc sans détailler on a une complexité temporelle en $O(log(n))$ pour gérer un évènement, avec $2n$ (les points des segments) $+ k$ (le nombre de points d'intersections) soit $O(n + k)$ évènements au total.
    En résumé, remplir la structure d'évènements prend un temps $O(nlog(n))$, chacun des $O(n + k)$ évènement prend un temps $O(log(n))$ et donc, avec $k = O(n)$, l'algorithme est en $O(nlog(n))$.
    Cependant si $k$ est très grand, en pratique l'algorithme naïf en $O(n^2)$ est plus rapide.

On peut faire d'autres observations concernant les segments :
 - Pour un segment AB quelconque, une intersection est possible ssi. les intervalles $[y0, y1]$ et $[yA, yB]$ se chevauchent.

    Cependant cette propriété n'est pas adaptée à une ligne car une ligne est infinie.


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

Passons à **l'inclusion en elle-même** (ie. ce que l'on effectue dans notre boucle).

L'algorithme PIP (Point In Polygon) évoqué dans le sujet a une complexité en $O(m)$ où $m$ est le nombre de segments du polygone.
$m$ représentera par la suite le nombre moyen de segments par polygone.

> Certaines propriétés des polygones permettent de simplifier des algorithmes. Il est ainsi possible de vérifier si un point se trouve dans un polygone **convexe** en $O(log(m))$ (Voir annexe a.1.).

> Ici cependant, nous avons aussi des polygones concaves. On a alors le choix entre utiliser un autre algorithme fonctionnant sur des polygones concaves ou alors découper notre polygone concave en polygones convexes (trigonalisation). Nous n'avons pas utilisé cette dernière approche.

La complexité temporelle avec cet algorithme est en $O(m.\frac{n(n - 1)}{2})$ dans le pire cas (zéro ou une unique inclusion par polygone). On peut chercher maintenant à réduire le nombre d'appels à l'algorithme PIP.

La **méthode des quadrants** présente dans le module $geo$ peut nous y aider. En effet, si les *bounding boxes* des polygones ne s'intersectent pas, alors il n'y aura pas d'inclusions entre ces polygones.

Cela nous rajoute une étape de prétraitement en $O(n.m)$ lors de laquelle on calcule les *bounding boxes* de chaque polygone. Puis une comparaison en $O(1)$ :
```
b1.min_x < b2.max_x and b1.max_x > b2.min_x and b1.min_y < b2.max_y and b1.max_y > b2.min_y
```
S'il n'y a aucune intersection entre les *bounding boxes*, cela fait une complexité en $O(n.m + \frac{n(n - 1)}{2})$ (on n'appelle pas l'algorithme PIP). Si toutes les *bounding boxes* s'intersectent, on appelle à chaque tour l'algorithme PIP et la complexité temporelle est donc en $O(n.m + m\frac{n(n - 1)}{2})$. Dans le cas où on n'a que des inclusions multiples, les *bounding boxes* s'intersectent toutes entre elles et la complexité temporelle est en $O(n.m + m.(n - 1))$.

---

Revenons sur le cas des polygones convexes. Il est possible de vérifier qu'un polygone est convexe en $O(m)$ (indépendamment de s'il est simple ou non d'ailleurs). On peut effectuer cette opération sur les $n$ polygones avant d'entrer dans la boucle de comparaison (voir annexe a.2.), puis utiliser notre algorithme en $O(log(m))$ sur ces polygones.

On aurait alors une complexité en $O(n.m + log(m).\frac{n(n - 1)}{2})$ si tous nos polygones étaient convexes.

### Algorithmes PIP

Dans ce paragraphe nous allons développer différentes implémentations de l'algorithme PIP.

Le principe de l'algorithme PIP évoqué dans le sujet est de boucler sur les segments du polygone $1$ et de **compter les intersections** avec une ligne passant par le point du polygone $2$.

On cherche donc à diminuer le nombre de segments pour itérer seulement sur ceux pouvant s'intersecter avec la ligne.

On peut se poser deux questions :
 - comment choisir le point du polygone $2$?
 - comment choisir la ligne passant par ce point ?

Nous ferons le choix ici de ne compter que les intersections d'abscisses inférieures à l'abscisse du point choisi. Si ce nombre est impair, le point est dans le polygone.

De ce choix découle que l'on peut minimiser le nombre d'intersections calculées en prenant le point du polygone $2$ d'abscisse minimale, et ne considérer que les segments du polygone $1$ dont les points sont d'abscisses inférieures à cette abscisse maximale. Avec un tri des segments, on peut sortir directement de la boucle sur les segments dès que l'on rencontre un segment dont les deux points sont d'abscisses supérieures à l'abscisse maximale.

Pour éviter d'avoir à calculer d'autres points d'intersections inutiles, on utilise la seconde observation du paragraphe *Intersection d'une ligne avec $n$ segments*. C'est une addition optionnelle.
Elle se traduit par :
```python
ecart0, ecart1 = y0 - y, y1 - y
if ecart0 * ecart1 > 0 or ecart0 == ecart1 == 0:
   continue
```

Ce qui nous importe ici ne sont pas les intersections mais leur nombre. Il existe plusieurs méthodes de décompte.
La méthode que nous avons utilisé choisi de ne compter que les intersections "supérieures" ou "inférieures" selon le test utilisé.
```python
(y0 >= ordo > y1 or y1 >= ordo > y0)  # n'ajoute que les traits qui traversent la ligne y et ceux qui arrivent d'en bas avec une extrémité sur la ligne y
(y0 > ordo >= y1 or y1 > ordo >= y0)  # n'ajoute que les traits qui traversent la ligne y et ceux qui arrivent d'en haut avec une extrémité sur la ligne y
```
L'inconvénient de cette méthode est que l'on perd des points d'intersections et donc possiblement des polygones. Si l'on est intéressé par l'ensemble des polygones s'intersectant avec la ligne $y$ on est obligé d'effectuer les deux tests, calculant ainsi des points d'intersections en double.

On peut penser à une autre méthode de décompte, nécessitant de connaître l'orientation entre deux segments successifs. Il est alors nécessaire de calculer celle-ci avant d'effectuer le tri des segments (ou alors de ne pas trier les segments). On raisonne ensuite par disjonction de cas : traversée de haut en bas, traversée de bas en haut, segment confondu avec la ligne (deux sous-cas ici, selon que les segments précédent et suivant aillent du même côté ou non de la ligne), coin supérieur et coin inférieur (DESSIN).

On peut maintenant calculer l'abscisse du point d'intersection et tester si elle est plus petite que celle du point du polygone $2$. Ci-dessous la formule déterminant l'abscisse du point d'intersection :
```python
interx = x1 + (ordo - y1) / (y0 - y1) * (x0 - x1)
```

---

La méthode précédente se prête aux erreurs numériques (et possiblement une division par 0 si l'on change les conditions du $if$ sans faire attention) lors du calcul de l'intersection. Il est possible de ne pas réaliser ce calcul.

On peut utiliser un simple compteur auquel l'on ajoute $1$ lorsque que l'on coupe la ligne vers le haut et un $-1$ si on la coupe vers le bas. Il faut aussi prendre en compte si le point est placé à gauche ou à droite du segment orienté et faire un choix : ne compter que les segments situés à gauche du point ou seulement ceux situés à sa droite.

Déterminer la position relative d'un point par rapport à une ligne peut se faire par un simple calcul d'aire signé.
```python
(x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
```
Si cette aire est positive (resp. négative), le point 2 à gauche (resp. droite) du segment orienté $[p0, p1]$.

---

L'ensemble des algorithmes PIP se trouve dans le fichier $algos_pip.py$.

## Une autre approche

Nous avons répondu à la première question posée au début du paragraphe précédent (pour rappel : comment choisir le point ?) et nous avons décidé de prendre une droite horizontale en réponse à la seconde question. Notez que nous aurions tout aussi bien pu choisir une ligne verticale.

Jusqu'ici nous avons tracé une droite par polygone alors qu'il est possible (même très fortement probable) qu'une même droite traverse plusieurs polygones.

On recherche alors **le plus petit ensemble de droites** tel que chaque droite s'intersecte avec plusieurs polygones.
Pour nous simplifier la vie, on suppose toujours que les droites sont horizontales.

> Quelle différence(s) y aurait-il eu à choisir des droites verticales ? Pour répondre à cette question il faut se ramener à des exemples précis du même type que les fichiers `upper_and_left_duplication.poly`. En effet, avec une ligne horizontale de polygones, on obtiendra une seule ligne horizontale et autant de lignes verticales qu'il y a de groupes de polygones inclus les uns dans les autres. C'est l'inverse pour une ligne verticale de polygones. Alors faut-il avoir le plus possible de lignes ou le moins possible ? ça dépend de ce que l'on compte en faire...

---

On se retrouve avec une liste de couples droite / liste de polygones. Pour chaque droite, on peut appliquer l'algorithme précédent à la liste de polygones correspondante.

Analysons l'étape de précalcul de l'ensemble de droite.

Dans le pire des cas on se retrouve avec une droite par polygone (ie. $n$ polygones alignés verticalements sans inclusions) et une complexité en $O(n^2)$. Dans le meilleur des cas on a une seule droite (ie. $n$ polygones alignés horizontalements) et une complexité en $O(n)$.

Sinon, on note $k$ le nombre de polygones traversés par la même ligne et $r$ le nombre de nouveaux (ie. qu'on a pas encore rencontré parmi tous les $k$ précédents) polygones parmi ces $k$ polygones on a une complexité en $O(r.k)$.

On a ensuite notre traitement en $O(p(m - 1) + \frac{n(n - 1)}{2})$ pour une moyenne de $p$ appels à l'algorithme PIP (ie. $p$ intersections de *bounding boxes*, le nombre d'appels allant de $0$ à $\frac{n(n - 1)}{2}$) - effectué pour chaque ligne.

En résumé pour $l$ lignes, on a une complexité en $O(n.m + r.k + l.\big(p(m - 1) + \frac{n(n - 1)}{2}\big)$.

---

Cela semble moins intéressant que notre première approche. Néanmoins nous n'avons pas développé la complexité des tris utilisés.

Avec notre première approche, on effectue un unique tri par aire sur les $n$ polygones en prétraitement.

Dans cette nouvelle approche, on effectue un tri par la valeur de l'ordonnée maximale des points du polygone sur les $n$ polygones en prétraitement. Mais ce n'est pas l'unique tri effectué. On tri ensuite par aire les $k$ polygones traversés par la même ligne à chaque itération sur l'ensemble des lignes.

Faire un nombre plus élevé de tri sur un ensemble de valeurs plus restreint semble plus efficace avec l'algorithme *Timsort* que de faire un unique tri sur toutes les valeurs.

---

On peut encore avoir une autre approche nécessitant de modifier notre fonction PIP. Celle-ci renverra la liste des points d'intersections entre la ligne et les segments des polygones. On effectuerait ensuite le comptage du nombre d'intersections.

Nous avons développé une ébauche fonctionnelle d'algorithme réalisant cette approche. Nous avons rencontré des problèmes pour récupérer le bon nombre d'intersections et n'avons pas développé d'algorithme efficace permettant de relever toutes les intersections en un seul appel.

Une piste d'amélioration serait d'inclure tous les compteurs des polygones d'une même ligne dans la fonction PIP.

## Mesures temporelles ou comparaisons expérimentales

On cherche ici à minimiser les erreurs systématique et aléatoire. Pour plus d'information sur la méthode utilisée consulter ce [lien](https://github.com/NicovincX2/python-tools/blob/master/measuring-code-execution-time.md).


Consulter le fichier $empirical_complexity.py$ pour plus d'informations sur les figures.

---

Nous allons commencer par tester les algorithmes du fichier $algos_pip.py$ pour chaque algorithme du fichier $algos_trouve_inclusions.py$ ayant un de ces algorithmes en paramètres.

Nous effectuerons ces tests avec les fichiers e2, 10x10, overlapping_square_1000 et upper_and_left_duplication_64 (n'hésitez pas à consulter les courbes du dossier $tests1/$ pour vous faire votre propre idée).

On constate que la fonction trouve_inclusions est la plus lente comme prévu. Elle permet d'avoir un ensemble de point suivant bien la droite de régression.

La fonction crossing_number_v3_segments apparaît comme très lente pour la fonction trouve_inclusions. On peut l'expliquer par le tri sur les segments et le fait que l'on boucle sur les segments et non pas les points.

Les fonctions crossing_number_v3_sec, crossing_number_v5 et winding_number sont les plus rapides.

Les fonctions autres que trouve_inclusions donnent des résultats peu exploitables pour les petits fichiers (e2 et 10x10).

---

Nous allons conserver les algorithmes crossing_number_v3_sec, crossing_number_v5 et winding_number ainsi que trouve_inclusions_sorted1, trouve_inclusions_sorted2 et trouve_inclusions_groupy1.

Nous effectuerons les tests avec le fichier plus conséquent upper_and_left_duplication_256.

Les résultats sont mitigés. Aucun des trois algorithmes PIP ne semble se démarquer. Nous allons donc grouper en fonction des meilleurs performances : le winding_number pour trouve_inclusions_groupy1, le crossing_number_v3_sec pour trouve_inclusions_sorted1 et crossing_number_v5 pour trouve_inclusions_sorted2.

---

Nous allons garder à l'esprit le groupement décelé lors du test précédent et fixer l'algorithme winding_number pour commencer. Nous testerons ensuite les deux autres algorithmes.

Observons les temps d'exécutions sur le fichier upper_and_left_duplication_256:

La première ligne correspond à trouve_inclusions_sorted1, la seconde à trouve_inclusions_sorted2 et la troisième à trouve_inclusions_groupy1.

winding_number
$$
[574114008, 1139859786, 1722721197, 2327846641, 2981675013, 4065701911, 4328074542]
The execution time is: (0.0, 656.0, 161.0, 416.7142858505249)
[775713111, 1548904539, 2312957580, 3301711726, 3743966787, 4518493082, 5250254591]
The execution time is: (0.0, 742.0, 636.0, 97.60714292526245)
[287784533, 576518753, 1044934474, 1204057370, 1447223241, 1865730313, 2057459417]
The execution time is: (0.0, 296.0, 62.0, 19.25)
$$
crossing_number_v3_sec
$$
[581914736, 1148200841, 1761292603, 2336870267, 2908719767, 3508070288, 4063955075]
The execution time is: (0.0, 582.0, 617.0, 395.5357142686844)
[752642838, 1497954808, 2264829637, 3026780991, 3747005773, 4537128798, 5252406197]
The execution time is: (0.0, 752.0, 136.0, 221.17857146263123)
[278784324, 554542920, 832403378, 1095390518, 1380842134, 1651239728, 1924956587]
The execution time is: (0.0, 274.0, 298.0, 184.32142859697342)
$$
crossing_number_v5
$$
[943716122, 1503821995, 2119504416, 2620455161, 3034968277, 4367255650, 4658518544]
The execution time is: (0.0, 635.0, 240.0, 658.4642856121063)
[750991184, 1744761843, 2546888378, 3607144305, 4087606970, 4826053333, 5727942712]
The execution time is: (0.0, 808.0, 362.0, 719.8571429252625)
[272765822, 536513685, 818223879, 1066324472, 1352387644, 1621397318, 1888779382]
The execution time is: (0.0, 269.0, 713.0, 275.3928571343422)
$$

Il apparaît que l'algorithme crossing_number_v3_sec est globalement le plus efficace sur cette entrée. Cette observation est vérifiée sur l'entrée 147_polygons_without_overlap.

Cet algorithme semble plus stable (bonne droite de régression) sur de grosses entrée que les deux autres. Il semble avoir la même stabilité sur des entrées plus petites.

Nous avons pu observer un classement des algorithmes : trouve_inclusions_groupy1, trouve_inclusions_sorted1 puis trouve_inclusions_sorted2 du plus au moins rapide.

Pour le fichier 147_polygons_without_overlap ne contenant aucune inclusion, les algorithmes trouve_inclusions_sorted1 et trouve_inclusions_sorted2 s'exécutent en temps similaires.

---

Nous conservons les algorithmes trouve_inclusions_sorted1 et trouve_inclusions_groupy1 avec l'algorithme PIP crossing_number_v3_sec.

Nous allons tester les fichiers e2, 10x10, 2_circular_shape, 25_polygons_around_1complex_shape, overlapping_square_4 / 100 / 1000 / 10000 et upper_and_left_duplication_2 / 64 / 256 / 512.

On observe que pour les petits fichiers e2, 10x10 et 2_circular_shape l'algorithme trouve_inclusions_sorted1 est étonnament plus rapide.

Pour le fichier 25_polygons_around_1complex_shape il est clairement plus rapide.

On peut maintenant consulter les examples du type overlapping_square et upper_and_left_duplication. On observe bien que trouve_inclusions_sorted1 est particulièrement bien adapté à overlapping_square tandis que trouve_inclusions_groupy1 l'est pour upper_and_left_duplication.

En résumé, il existe des cas où il est inutile de partitionner par rapport à une ligne horizontale.

Il serait intéressant de réaliser un algorithme similaire avec une ligne verticale pour observer les possibles différences.

## Générateurs d'entrées

S'il est important de distinguer le comportement asymptotique du temps d'exécution réelle de notre algorithme, c'est en partie parce que les paramètres en entrée sont déterminants.

Nous n'avons pas souhaité développer des algorithmes de génération d'un ensemble quelconque de polygones.
Nous avons cherché les cas qui pourraient poser problème à nos algorithmes et programmé des duplicateurs étant capables de les créer.

Nous pouvons actuellement générer :
 - l'inclusion d'un très grand nombre de polygones,
 - la duplication d'un ensemble de polygones selon l'axe des ordonnées, l'axe des abscisses ou les deux axes,

Dans nos essais (infructueux...) de création de générateur d'entrée nous avons rencontré plusieurs problèmes :
 - éviter les intersections de segments lors de la génération des segments,
 - effectuer une bonne jonction entre le premier et le dernier point, 

Le fichier `polygones_generator.py` présent sur notre répertoire du projet contient nos pistes d'algorithmes et un algorithme fonctionnel trouvé sur internet que nous avons testé.

## Conclusion

Nous avons développé plusieurs algorithmes fonctionnels répondant au problème posé et effectué une analyse à la fois asymptotique et expérimentale de ces algorithmes.

Il est difficile de trouver des optimisations indépendantes les une des autres. L'utilisation simultanée de plusieurs optimisations peut alors se révéler moins performante que l'algorithme initial non optimisé.

Merci d'avoir pris le temps de lire (ou survoler) ce rapport.

## Annexes
a.1.
- Une approche est de trianguler le polygone en traçant les arêtes d'un sommet à tous les autres, trouver l'angle où se trouve le point en utilisant une recherche dichotomique et ensuite vérifier si le point est dans le triangle ou non.
- On peut penser à une autre approche. Si le point est en dessous (ou à gauche sur la même droite horizontale) que le sommet inférieur (ie. le sommet de plus petite ordonnée) gauche, le sommet est hors du polygone. On a le même raisonnement pour le sommet supérieur droit. On connecte ces deux sommets. Si le point est sur ce segment, il est soit sur la limite du polygone (confondu avec les extrémités du segment ou sinon ce segment est une arête du polygone), soit à l'intérieur du polygone. Si le point est à droite (ou à gauche de manière analogue), nous devons vérifier s'il se trouve à gauche de la chaîne droite construite par l'algorithme du calcul de l'enveloppe convexe. L'arrête correspondante est trouvée en utilisant la recherche dichotomique, en comparant les points lexicographiquement.

a.2.

*(Quick and)* **Dirty** : `[all((a - c) * (d - f) <= (b - d) * (c - e) for (a, b), (c, d), (e, f) in zip(p[-2:] + p, [p[-1]] + p + [p[0]], p))::2]` où $p$ est une liste de points.

Voir [ce post](https://stackoverflow.com/a/1881201) pour plus d'informations.

a.3. 

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
 - crossing_number, crossing_number_v2, crossing_number_v3, crossing_number_v3_sec, crossing_number_v3_segments, winding_number, crossing_number_v5
 - trouve_inclusions, trouve_inclusions_sorted1, trouve_inclusions_sorted2, trouve_inclusions_groupy1, trouve_inclusions_groupy2 (avec et sans test des quadrants)