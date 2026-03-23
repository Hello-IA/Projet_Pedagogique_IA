from collections import deque


def bfs(grid, start, goal, ROWS, COLS):
    # queue : crée une file d'attente où le premier arrivé est aussi le premier à repartir
    queue = deque([start])
    # visited : contient tous les nœuds déjà visités pour éviter de les visiter plusieurs fois
    visited = set([start])
    # ici, on sauvegarde depuis quel nœud on a découvert un nouveau nœud afin de pouvoir retrouver le chemin qui y mène
    parent = {}
    while queue:
        # on récupère l'objet à l'avant de la file d'attente
        current = queue.popleft()
        
        if current == goal:
            break
        # on récupère les coordonnées de cet objet
        x, y = current
        # calcule la liste des voisins
        neighbors = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        # parcourt les 4 voisins
        for nx, ny in neighbors:
            # vérifie qu'ils sont bien dans les limites de la grille
            if 0 <= nx < ROWS and 0 <= ny < COLS:
                 # vérifie que ce ne sont pas des murs et qu'ils ne sont pas déjà visités
                if grid[nx][ny] != 0 and (nx, ny) not in visited:
                    # ajoute le voisin à la file d'attente
                    queue.append((nx, ny))
                    # ajoute le voisin à l'ensemble des nœuds visités
                    visited.add((nx, ny))
                    # indique que le voisin exploré a été trouvé depuis le nœud courant
                    parent[(nx, ny)] = current
        
        yield ("Exploration", current) # permet une animation frame par frame

    # reconstruction du chemin
    node = goal
    while node in parent:
        node = parent[node]
        yield ("path", node)
