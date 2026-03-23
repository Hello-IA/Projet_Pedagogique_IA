import math
def Dijkstra(grille, depart, objectif, LIGNES, COLONNES):
    
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
    
    # ici, on sauvegarde depuis quel nœud on doit venir pour obtenir la distance la plus courte à un nœud depuis le départ 
    parent = {}
    
    # on conserve l'ensemble des nœuds non explorés
    non_visite = set()
    for y in range(COLONNES):
        for x in range(LIGNES):
            non_visite.add((x, y))
    

    
    while non_visite:
        # parmi tous les nœuds non visités, on prend celui qui a la distance la plus petite
        courant = None
        distance_min = math.inf

        for noeud in non_visite:
            x, y = noeud
            
            if distance[x][y] < distance_min:
                distance_min = distance[x][y]
                courant = noeud
                
        # vérifie qu'on n'explore pas un nœud avec une distance infinie (cas qui arrive quand il n'y a pas de chemin possible)        
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
                
                # calcule la distance au nœud voisin en passant par le nœud courant
                distance_alternative = distance[x][y] + grille[vx][vy]
                
                # vérifie que ce ne sont pas des murs et que le nouveau chemin n'est pas pire que l'ancien
                
                if grille[vx][vy] != MUR and distance_alternative < distance[vx][vy]:
                    
                    # si le nouveau chemin est meilleur que l'ancien, on sélectionne le nouveau chemin
                    distance[vx][vy] = distance_alternative
                    
                    # et on remplace le parent du voisin pour l'inclure dans le nouveau chemin
                    parent[(vx, vy)] = courant
        
        
                    
        yield ("Exploration", courant) # permet animation frame par frame
        
    # on remonte le chemin depuis l'objectif jusqu'au départ
    noeud = objectif
    while noeud in parent:
        noeud = parent[noeud]
        yield ("path", noeud)
    