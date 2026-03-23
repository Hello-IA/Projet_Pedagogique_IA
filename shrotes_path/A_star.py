import math

# fonction heuristique (distance de Manhattan)
def heuristique(a, objectif):
    # renvoie la somme des distances absolues sur x et y
    return abs(a[0] - objectif[0]) + abs(a[1] - objectif[1])

def A_star(grille, depart, objectif, LIGNES, COLONNES):
    
    MUR = 0
    
    # la matrice des distances à la case de départ
    distance = []
    for _ in range(LIGNES):
        ligne = []
        for _ in range(COLONNES):
            ligne.append(math.inf)
        distance.append(ligne)
    
    # les coordonnées de la case de départ
    depart_x, depart_y = depart
    
    # la distance de la case de départ à elle-même est de 0
    distance[depart_x][depart_y] = 0
    
    # ici, on sauvegarde depuis quel nœud on doit venir pour obtenir la distance la plus courte
    parent = {}
    
    # on conserve l'ensemble des nœuds non explorés
    non_visite = set()
    for x in range(LIGNES):
        for y in range(COLONNES):
            non_visite.add((x, y))
    
    while non_visite:
        # parmi tous les nœuds non visités, on prend celui qui a la plus petite valeur f = distance + heuristique
        courant = None
        f_min = math.inf
        
        for noeud in non_visite:
            x, y = noeud
            
            # calcul de f pour ce nœud
            f_noeud = distance[x][y] + heuristique(noeud, objectif)
            
            if f_noeud < f_min:
                f_min = f_noeud
                courant = noeud
        
        # vérifie qu'on n'explore pas un nœud inaccessible
        if courant is None:
            break
        
        # on le retire des nœuds à visiter
        non_visite.remove(courant)
        
        # si le nœud courant est égal à l'objectif, on arrête la boucle
        if courant == objectif:
            break
        
        # on récupère les coordonnées de cet objet
        x, y = courant
        
        # calcule la liste des voisins
        voisins = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        
        # parcourt les 4 voisins
        for vx, vy in voisins:
            
            # vérifie qu'ils sont bien dans les limites de la grille
            if 0 <= vx < LIGNES and 0 <= vy < COLONNES:
                
                # calcule la distance au voisin en passant par le nœud courant
                distance_alternative = distance[x][y] + grille[vx][vy]
                
                # vérifie que ce n'est pas un mur et que le nouveau chemin est meilleur que l'ancien
                if grille[vx][vy] != MUR and distance_alternative < distance[vx][vy]:
                    
                    # on met à jour la distance
                    distance[vx][vy] = distance_alternative
                    
                    # et on met à jour le parent
                    parent[(vx, vy)] = courant
        
        # permet animation frame par frame
        yield ("Exploration", courant)
    
    # on remonte le chemin depuis l'objectif jusqu'au départ
    noeud = objectif
    while noeud in parent:
        noeud = parent[noeud]
        yield ("path", noeud)