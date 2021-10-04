from heapq  import heappop, heappush

def debut(cours):
    return cours[0]

def fin(cours):
    return cours[1]

def algo_naif(H):
    # Cas trivial  O(1)
    if len(H) == 0:
      return 0    
    
    # Identifier le tout premier et tout dernier moment  O(n)
    a = +float("inf")
    b = -float("inf")
    
    for cours in H:
        a = min(a, debut(cours))
        b = max(b, fin(cours))
      
    # Calculer le nombre de salles requis pour chaque moment  O((b - a)·n)
    num_salles = 0

    for moment in range(a, b+1):
      c = 0

      for cours in H:
        if debut(cours) <= moment < fin(cours):
          c = c + 1
      
      num_salles = max(num_salles, c)
      
    return num_salles

def algo_quadratique(H):
    # Identifier tous les moments où débutent au moins un cours  O(n)
    moments = set()
   
    for cours in H:
        moments.add(debut(cours))
      
    num_salles = 0

    # Calculer le nombre de salles requis pour chaque moment  O(n²)
    for moment in moments:
      c = 0

      for cours in H:
        if debut(cours) <= moment < fin(cours):
          c = c + 1
      
      num_salles = max(num_salles, c)
      
    return num_salles

def algo_local(H):
    # Cas trivial  O(1)
    if len(H) == 0:
      return 0
      
    # Ordonner les cours  O(n log n)
    H = list(sorted(H))

    # Compter le nombre de salles selon les conflits locaux  O(n)
    num_salles = 1

    for i in range(1, len(H)):
      if debut(H[i]) < fin(H[i-1]):
          num_salles = num_salles + 1
          
    return num_salles

def algo_lineaire(H):
    # Ordonner les moments  O(n log n)
    moments = [(fin(cours),   0) for cours in H] + \
              [(debut(cours), 1) for cours in H]

    moments = list(sorted(moments))

    # Assigner et libérer itérativement les salles  O(n)
    num_salles = 0
    num_salles_actives = 0

    for (temps, type_) in moments:
        num_salles_actives += (1 if (type_ == 1) else -1)
        
        num_salles = max(num_salles, num_salles_actives)
          
    return num_salles

def algo_monceau(H):
    # Ordonner les cours  O(n log n)
    H = list(sorted(H))

    # Libérer et assigner les salles  O(n log n)
    salles = []
    
    num_salles = 0
  
    for cours in H:
        while (len(salles) > 0) and (salles[0] <= debut(cours)):
            heappop(salles)
          
        heappush(salles, fin(cours))
      
        num_salles = max(num_salles, len(salles))
          
    return num_salles

if __name__ == "__main__":
    def tester(H):
        algos = [algo_naif, algo_quadratique, algo_local,
                 algo_lineaire, algo_monceau]

        print("Horaire:", H)
        print()

        for algo in algos:
            print("{:>17}(s) = {}".format(algo.__name__, algo(H)))

        print()

    tester([(0, 5), (1, 12), (8, 11), (3, 8),
            (12, 14), (13, 15), (18, 20), (1, 16)])

    tester([(0, 3), (1, 4), (2, 5), (3, 6)])

    tester([(0, 2), (1, 3), (4, 6), (5, 7)])
