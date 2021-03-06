# Assignation de salles

Ce billet discute de différentes approches afin de résoudre le problème qui consiste à déterminer
le nombre de salles minimal qui satisfait un horaire de cours. Une implémentation en Python de chaque procédure qui sera
décrite se trouve dans [```implementations.py```](implementations.py).

## Un algorithme inefficace qui fonctionne

Une toute première approche consiste à: (a) identifier tous les moments
de l'horaire; (b) balayer la plage des moments; (c) vérifier à chaque
moment le nombre de salles requis. Par exemple, si ```H = [(0, 3), (1,
4), (2, 5), (3, 6)]```, alors l'ensemble des moments est _{0, 1, 2,
3, 4, 5, 6}_. On itère ensuite sur chaque moment, et on vérifie la
quantité de cours qui nécessitent une salle à ce moment précis. Sous
forme de pseudocode, nous obtenons:

```
  algo_naif(H):
    // Identifier le tout premier et tout dernier moment  O(n)
    a ← +∞
    b ← -∞
   
    pour cours ∈ H:
      a = min(a, debut(cours))
      b = max(b, fin(cours))
      
    // Calculer le nombre de salles requis pour chaque moment  O((b - a)·n)
    num_salles ← 0

    pour moment ∈ [a..b]:
      c ← 0

      pour cours ∈ H
        si debut(cours) ≤ moment < fin(cours):
          c ← c + 1
      
      num_salles = max(num_salles, c)
      
    retourner num_salles
```

Cet algorithme fonctionne, mais son temps d'exécution est
arbitrairement mauvais par rapport à _n_. En effet, considérons par
ex. la famille d'entrées ```[(0, 1), (m-2, m-1)]```. Il y a exactement
_m_ moments distincts et deux cours. Ainsi, en augmentant _m_, on
obtient un temps de plus en plus long, sans changer le nombre de cours.

En fait, si _i_ dénote le nombre de bits qui permet de décrire un
cours, alors l'algorithme fonctionne en temps _O(2ⁱ·n)_ car il risque
d'énumérer tous les nombres de _i_ bits.

## Un algorithme quadratique qui fonctionne

On peut adapter l'approche précédente afin qu'elle soit plus rapide. Il
suffit de ne considérer que les ***moments pertinents***. Par exemple,
si un cours débute au moment 0, se termine au moment 100, et qu'aucun
cours ne débute entre temps, alors il n'y a aucun intérêt à considérer
les moments 1 à 99. Ainsi, on peut se limiter aux débuts de cours, ce
qui mène à un temps d'exécution de _O(n·n) = O(n²)_:

```
  algo_quadratique(H):
    // Identifier tous les moments où débutent au moins un cours  O(n)
    moments ← ∅
   
    pour cours ∈ H:
      ajouter debut(cours) à moments
      
    num_salles ← 0

    // Calculer le nombre de salles requis pour chaque moment  O(n²)
    pour moment ∈ moments:
      c ← 0

      pour cours ∈ H
        si debut(cours) ≤ moment < fin(cours):
          c ← c + 1
      
      num_salles = max(num_salles, c)
      
    retourner num_salles
```

## Un algorithme plus efficace qui ne fonctionne pas

Nous pouvons espérer faire mieux en diminuant la complexité à _O(n log
n)_. Dans un premier temps, nous pourrions trier les cours en ordre
croissant selon le moment de début, puis selon le moment de fin en
bris d'égalité. Il serait ensuite tentant de procéder ainsi: on itère sur
chaque cours, et on alloue une nouvelle salle si on crée un conflit
avec le cours précédent:

```
  algo_local(H):
    // Cas trivial  O(1)
    si n = 0:
      retourner 0
      
    // Ordonner les cours  O(n log n)
    trier H en ordre croissant selon le début, puis selon la fin en bris d'égalité

    // Compter le nombre de salles selon les conflits locaux  O(n)
    num_salles ← 0

    pour i ∈ [2..n]:
      si debut(H[i]) < fin(H[i-1]):
        num_salles ← num_salles + 1
          
    retourner num_salles
```

Toutefois, cela ne fonctionne pas. Par exemple, considérons l'entrée
```H = [(0, 3), (1, 4), (2, 5), (3, 6)]``` en «forme
d'escalier». L'algorithme retourne ```4```, alors que la solution est
```3```. Le problème est que l'algorithme raisonne trop «localement»;
lorsqu'il atteint le quatrième cours, il ne réalise pas que le premier
cours vient de se terminer. En fait, cet algorithme ne libère jamais
de salle. Par exemple, sur entrée ```H = [(0, 2), (1, 3), (4, 6), (5,
7)]```, la procédure retourne ```3``` plutôt que ```2```. En effet,
lorsque les deux premiers cours sont terminés, on devrait décrémenter
le nombre de salles, alors que l'algorithme continue d'incrémenter.

## Un algorithme efficace qui fonctionne

Nous pouvons combiner les idées précédentes afin d'obtenir un
algorithme à la fois efficace et correct. L'idée consiste à
répertorier tous les moments pertinents, en gardant en tête leur type:
«fin de cours» (type 0) ou «début de cours» (type 1). Nous
considérons les fins de cours comme prioritaires, car lorsqu'un cours _c_
termine au moment _j_ et qu'un autre cours _c'_ débute au moment _j_,
nous pouvons libérer la salle de _c_ puis l'assigner à _c'_.

L'approche est décrite comme suit:

```
  algo_lineaire(H):
    // Ordonner les moments  O(n log n)
    moments ← [(fin(cours), 0) : cours ∈ H] + [(debut(cours), 1) : cours ∈ H]

    trier moments en ordre croissant selon 1ère composante, puis selon 2e en bris d'égalité

    // Assigner et libérer itérativement les salles  O(n)
    num_salles ← 0
    num_salles_actives ← 0

    pour (temps, type) ∈ moments:
      si (type = 0):
        num_salles_actives ← num_salles_actives - 1
      sinon:
        num_salles_actives ← num_salles_actives + 1
        
      num_salles = max(num_salles, num_salles_actives)
          
    retourner num_salles
```

## Un autre algorithme efficace qui fonctionne

L'idée précédente peut être implémentée différemment à l'aide d'un
monceau binaire. On trie d'abord les cours en ordre croissant de
début, puis de fin en bris d'égalité. On initialise ensuite un monceau
vide, puis on itère sur les cours. À chaque nouveau cours _c_, on
libère toutes les salles qui contiennent un cours terminé, puis on
alloue une nouvelle salle pour _c_. Sous forme de pseudocode, nous
obtenons cette procédure:

```
  algo_monceau(H):
    // Ordonner les cours  O(n log n)
    trier H en ordre croissant selon 1ère composante, puis selon 2e en bris d'égalité

    // Assigner et libérer itérativement les salles  O(n)
    salles ← monceau vide
    
    num_salles ← 0
  
    // Libérer et assigner les salles  O(n log n)
    pour cours ∈ H:
      tant que (|salles| > 0) ∧ (min(salles) ≤ debut(cours)):
        retirer élément mininimal de salles
      
      ajouter fin(cours) à salles
      
      num_salles ← max(num_salles, |salles|)
          
    retourner num_salles
```
