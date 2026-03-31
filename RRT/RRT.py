import random
import math


def proche_voisin(arbre, q_rand):
    argmin_dis = None
    dis_min = math.inf
    for v in arbre.keys():
        dist_v = math.sqrt((v[0]-q_rand[0])**2 + (v[1]-q_rand[1])**2)
        if dist_v < dis_min:
            dis_min = dist_v
            argmin_dis = v
    return argmin_dis
        
        
        
def diriger(q_near, q_rand, step_size):
    dx = q_rand[0] - q_near[0]
    dy = q_rand[1] - q_near[1]
    dist = math.sqrt(dx**2 + dy**2)
    if dist == 0:
        return q_near
    

    dx_unit = dx / dist
    dy_unit = dy / dist
    x_new = q_near[0] + step_size * dx_unit
    y_new = q_near[1] + step_size * dy_unit
    return x_new, y_new

def interpolate(q1, q2, t):

    x1, y1 = q1
    x2, y2 = q2

    x = (1 - t) * x1 + t * x2
    y = (1 - t) * y1 + t * y2

    return (x, y)

def collision(grille, x, y, ROWS, COLS, CELL_SIZE):
        
        if 0 <= x and x < ROWS*CELL_SIZE and 0 <= y and y < COLS*CELL_SIZE:
            return grille[int(x//CELL_SIZE)][int(y//CELL_SIZE)] == 0
        return True
def vecteur_libre(grille, q1, q2,  ROWS, COLS, CELL_SIZE):
    for i in range(0, 11):
        t = i/10
        point = interpolate(q1, q2, t)
        if collision(grille, point[0], point[1], ROWS, COLS, CELL_SIZE):

            return False
    return True
            

def RRT(grille, start, goal, max_iter, step_size, ROWS, COLS, CELL_SIZE):

    arbre = {start: set()}
    parent = {}
    parent[start] = None
    i = 0
    pas_trouver = True
    while i < max_iter and pas_trouver:
        q_rand = (random.randint(0, ROWS*CELL_SIZE), random.randint(0, COLS*CELL_SIZE))
        
        q_near = proche_voisin(arbre, q_rand)
        
        q_new = diriger(q_near, q_rand, step_size)

        if vecteur_libre(grille, q_near, q_new, ROWS, COLS, CELL_SIZE):
            arbre[q_near].add(q_new)
            arbre[q_new] = set()
            parent[q_new] = q_near
            
            if math.sqrt((q_new[0] -goal[0])**2 + (q_new[1]-goal[1])**2) < step_size:
                if vecteur_libre(grille, q_new, goal, ROWS, COLS, CELL_SIZE):
                    parent[goal] = q_new
                    pas_trouver = False
            yield ("Exploration", arbre)
        i += 1
    if pas_trouver == False:
        point = goal
        while point in parent:
            point = parent[point]
            yield ("path", point)
        
            
        
        