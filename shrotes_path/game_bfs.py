import pygame
import sys
from BFS import *
from Dijkstra import * 
from A_star import *
# ===== PARAMETRES =====
CELL_SIZE = 15
ROWS, COLS = 40, 40

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + 100
algo_actif = "BFS"

score = 0
pygame.init()

# chargement du sprite pour les murs


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Éditeur BFS/Dijkstra/A*")

font = pygame.font.SysFont(None, 24)

sprite_eau = pygame.image.load("Tiles\\wather.png").convert_alpha()

# redimensionner à la taille d'une cellule
sprite_eau = pygame.transform.scale(sprite_eau, (CELL_SIZE, CELL_SIZE))

sprite_grass = pygame.image.load("Tiles\\grass.png").convert_alpha()

# redimensionner à la taille d'une cellule
sprite_grass = pygame.transform.scale(sprite_grass, (CELL_SIZE, CELL_SIZE))

sprite_montaine = pygame.image.load("Tiles\\montaine.png").convert_alpha()

# redimensionner à la taille d'une cellule
sprite_montaine = pygame.transform.scale(sprite_montaine, (CELL_SIZE, CELL_SIZE))

sprite_snow = pygame.image.load("Tiles\\snow.png").convert_alpha()

# redimensionner à la taille d'une cellule
sprite_snow = pygame.transform.scale(sprite_snow, (CELL_SIZE, CELL_SIZE))

# ===== ETAT =====
grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]

start = None
goal = None

mode = "edit"  # "edit" ou "run"

brightness = {}
path_cells = set()

# init brightness
def reset_visual():
    brightness.clear()
    path_cells.clear()
    for x in range(ROWS):
        for y in range(COLS):
            brightness[(x,y)] = 0.0

reset_visual()

bfs_gen = None

clock = pygame.time.Clock()

# ===== OUTILS =====
def get_cell_from_mouse(pos):
    x = pos[1] // CELL_SIZE
    y = pos[0] // CELL_SIZE
    return x, y

# ===== TERRAINS =====
terrains = [
    {"name":"Facile", "cost":1, "sprite":sprite_grass},   # bleu
    {"name":"Moyen",  "cost":3, "sprite":sprite_montaine},   # brun
    {"name":"Difficile","cost":5,"sprite":sprite_snow},   # rouge
]
terrain_actif = terrains[0]

def check_click_terrain(pos):
    for i, t in enumerate(terrains):
        rect = pygame.Rect(10 + i*60, 10, 50, 30)
        if rect.collidepoint(pos):
            return t
    return None


def check_click_algo(pos):
    buttons = ["BFS", "DIJKSTRA", "ASTAR"]
    for i, name in enumerate(buttons):
        rect = pygame.Rect(250 + i*110, 10, 100, 30)
        if rect.collidepoint(pos):
            return name
    return None


# ===== LOOP =====
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ===== CLIC SOURIS =====
        if mode == "edit":
            if pygame.mouse.get_pressed()[0]:  # clic gauche
                x, y = get_cell_from_mouse(pygame.mouse.get_pos())
                selection = check_click_terrain(event.pos)
                selection_algo = check_click_algo(event.pos)
                if selection_algo:
                    algo_actif = selection_algo
                elif selection:
                    terrain_actif = selection
                elif 0 <= x < ROWS and 0 <= y < COLS:
                    grid[x][y] = 0  # mur

            if pygame.mouse.get_pressed()[2]:  # clic droit
                x, y = get_cell_from_mouse(pygame.mouse.get_pos())
                if 0 <= x < ROWS and 0 <= y < COLS:
                    grid[x][y] = terrain_actif["cost"]  # enlever mur
            

        # ===== CLAVIER =====
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                x, y = get_cell_from_mouse(pygame.mouse.get_pos())
                start = (x, y)

            if event.key == pygame.K_g:
                x, y = get_cell_from_mouse(pygame.mouse.get_pos())
                goal = (x, y)

            if event.key == pygame.K_SPACE and start and goal:
                # lancer BFS
                mode = "run"
                reset_visual()
                score = 0
                if algo_actif == "DIJKSTRA":
                    bfs_gen = Dijkstra(grid, start, goal, ROWS, COLS)
                elif algo_actif == "ASTAR":
                    bfs_gen = A_star(grid, start, goal, ROWS, COLS)
                else:
                    bfs_gen = bfs(grid, start, goal, ROWS, COLS)
                    
                    
                    

            if event.key == pygame.K_r:
                mode = "edit"
                reset_visual()

    # ===== BFS =====
    if mode == "run" and bfs_gen:
        for _ in range(20):
            try:
                action, node,  = next(bfs_gen)

                if action == "Exploration":
                    brightness[node] = 1

                elif action == "path":
                    path_cells.add(node)
                    score += grid[node[0]][node[1]]

            except StopIteration:
                break

    # ===== DRAW =====
    screen.fill((0,0,0))

    for x in range(ROWS):
        for y in range(COLS):
            rect = pygame.Rect(y*CELL_SIZE, x*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            val = grid[x][y]
            if grid[x][y] == 0:
                #pygame.draw.rect(screen, (0,0,0), rect)
                # affiche le sprite à la place du mur
                screen.blit(sprite_eau, rect)
            else:
                terrain = next(t for t in terrains if t["cost"]==val)
                b = brightness[(x,y)]
                
                screen.blit(terrain["sprite"], rect)


                # bordure fine
                pygame.draw.rect(screen, (20,20,20), rect, 1)


            if (x,y) in path_cells:
                pygame.draw.rect(screen, (255,255,0), rect)
                # contour lumineux léger
                pygame.draw.rect(screen, (255,255,180), rect, 1)

    # start / goal
    if start:
        pygame.draw.rect(screen, (0,255,0),
            (start[1]*CELL_SIZE, start[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    if goal:
        pygame.draw.rect(screen, (255,0,0),
            (goal[1]*CELL_SIZE, goal[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    
    # ===== Panneau terrain =====
    for i, t in enumerate(terrains):
        rect = pygame.Rect(10 + i*60, 10, 50, 30)
        
        # si un sprite existe, on l'affiche
        if t["sprite"] is not None:
            sprite_redim = pygame.transform.scale(t["sprite"], (50, 30))
            screen.blit(sprite_redim, rect)
        else:
            # fallback couleur
            pygame.draw.rect(screen, t["color"], rect)
        
        # bordure si sélectionné
        if t == terrain_actif:
            pygame.draw.rect(screen, (255,255,255), rect, 3)
            
    buttons = ["BFS", "DIJKSTRA", "ASTAR"]

    for i, name in enumerate(buttons):
        rect = pygame.Rect(250 + i*110, 10, 100, 30)

        # couleur différente si actif
        if name == algo_actif:
            pygame.draw.rect(screen, (255,255,255), rect)
            text_color = (0,0,0)
        else:
            pygame.draw.rect(screen, (80,80,80), rect)
            text_color = (255,255,255)

        text = font.render(name, True, text_color)
        screen.blit(text, (rect.x + 10, rect.y + 5))
    # ===== TEXTE =====
    legend = [
        "Clic gauche = mur",
        "Clic droit = effacer",
        "S = départ | G = objectif",
        "SPACE = lancer BFS",
        "R = reset",
        f"Score : {score}"
    ]

    for i, text in enumerate(legend):
        img = font.render(text, True, (255,255,255))
        screen.blit(img, (10, ROWS*CELL_SIZE + 5 + i*15))

    pygame.display.flip()

pygame.quit()
sys.exit()