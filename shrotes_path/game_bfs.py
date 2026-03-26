import pygame
import sys
from BFS import *
from Dijkstra import * 
from A_star import *
import math



class Game:
    def __init__(self):
        # ===== PARAMETRES =====
        self.CELL_SIZE = 16
        self.ROWS, self.COLS = 40, 40

        self.WIDTH = self.COLS * self.CELL_SIZE
        self.HEIGHT = self.ROWS * self.CELL_SIZE + 140
        self.algo_actif = "BFS"

        self.path_casse = 0
        self.exp_casse = 0

        self.score = 0
        self.score_exp = 0

        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Éditeur BFS/Dijkstra/A*")

        self.font = pygame.font.SysFont(None, 24)

        self.TILE_SIZE = 16

        self.sprite_maptiles = pygame.image.load("Tiles\\maptiles.png").convert_alpha()

        width, height = self.sprite_maptiles.get_size()

        self.tiles = []

        for y in range(0, height, self.TILE_SIZE):
            row = []
            for x in range(0, width, self.TILE_SIZE):
                rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
                tile = self.sprite_maptiles.subsurface(rect)
                row.append(tile)
            self.tiles.append(row)

        rect = pygame.Rect(64, 80, 48, 48)
        self.grass = self.sprite_maptiles.subsurface(rect)

        rect = pygame.Rect(64, 144, 48, 48)
        self.montaine = self.sprite_maptiles.subsurface(rect)

        rect = pygame.Rect(128, 0, 48, 48)
        self.snow = self.sprite_maptiles.subsurface(rect)

        self.TILE_SIZE_UNIT = 32

        self.sprite_units = pygame.image.load("Tiles\\units.png").convert_alpha()

        width, height = self.sprite_units.get_size()

        self.units = []

        for y in range(0, height, self.TILE_SIZE_UNIT):
            row = []
            for x in range(0, width, self.TILE_SIZE_UNIT):
                rect = pygame.Rect(x, y, self.TILE_SIZE_UNIT, self.TILE_SIZE_UNIT)
                unit = self.sprite_units.subsurface(rect)
                row.append(unit)
            self.units.append(row)

        self.player_BFS = self.units[0][3]
        self.player_BFS = pygame.transform.scale(self.player_BFS, (self.CELL_SIZE, self.CELL_SIZE))

        self.sprite_castle = pygame.image.load("Tiles\\lilcastle.png").convert_alpha()

        rect = pygame.Rect(0, 0, 32, 32)
        self.castle = self.sprite_castle.subsurface(rect)
        self.castle = pygame.transform.scale(self.castle, (self.CELL_SIZE, self.CELL_SIZE))

        self.sprite_way = pygame.image.load("Tiles\\way.png").convert_alpha()
        self.way = pygame.transform.scale(self.sprite_way, (self.CELL_SIZE, self.CELL_SIZE))

        # ===== ETAT =====
        self.grid = [[1 for _ in range(self.COLS)] for _ in range(self.ROWS)]

        self.start = None
        self.goal = None

        self.mode = "edit"

        self.brightness = {}
        self.path_cells = set()
        self.path_parent = {}
        self.parent = None

        self.reset_visual()

        self.bfs_gen = None

        self.clock = pygame.time.Clock()

        # ===== TERRAINS =====
        self.terrains = [
            {"name":"Grass", "cost":1, "sprite":self.grass},
            {"name":"Montaine",  "cost":3, "sprite":self.montaine},
            {"name":"snow","cost":5,"sprite":self.snow},
        ]
        self.terrain_actif = self.terrains[0]

    def reset_visual(self):
        self.brightness.clear()
        self.path_cells.clear()
        self.path_parent.clear()
        self.parent = None
        for x in range(self.ROWS):
            for y in range(self.COLS):
                self.brightness[(x,y)] = 0.0

    def get_cell_from_mouse(self, pos):
        x = pos[1] // self.CELL_SIZE
        y = pos[0] // self.CELL_SIZE
        return x, y

    def check_click_terrain(self, pos):
        for i, t in enumerate(self.terrains):
            rect = pygame.Rect(10 + i*60, 10, 48, 48)
            if rect.collidepoint(pos):
                return t
        return None

    def generate_tiles(self, x, y, center, tl, bl, tr, br):
        voisin_8 = []
        for i in range(-1, 2):
            voisin = []
            for j in range(-1, 2):
                if 0 <= x+i < self.ROWS and 0 <= y+j < self.COLS:
                    val_voisin = self.grid[x+i][y+j]
                else:
                    val_voisin = math.inf
                voisin.append(val_voisin)
            voisin_8.append(voisin)
        tile = pygame.Surface((16, 16), pygame.SRCALPHA)

        tl_small, tr_small, bl_small, br_small = None, None, None, None
        val = self.grid[x][y]
        size = 8
        tl_small = pygame.transform.scale(self.tiles[center[0]][center[1]], (size, size))
        tr_small = pygame.transform.scale(self.tiles[center[0]][center[1]], (size, size))
        bl_small = pygame.transform.scale(self.tiles[center[0]][center[1]], (size, size))
        br_small = pygame.transform.scale(self.tiles[center[0]][center[1]], (size, size))

        if voisin_8[1][0] != val and voisin_8[0][1] != val:
            tl_small = pygame.transform.scale(self.tiles[tl[0][0]][tl[0][1]], (size, size))
        elif voisin_8[1][0] == val and voisin_8[0][1] == val and voisin_8[0][0] != val:
            tl_small = pygame.transform.scale(self.tiles[tl[1][0]][tl[1][1]], (size, size))
        elif voisin_8[1][0] != val and voisin_8[0][1] == val:
            tl_small = pygame.transform.scale(self.tiles[tl[2][0]][tl[2][1]], (size, size))
        elif voisin_8[1][0] == val and voisin_8[0][1] != val:
            tl_small = pygame.transform.scale(self.tiles[tl[3][0]][tl[3][1]], (size, size))

        if voisin_8[1][0] != val and voisin_8[2][1] != val:
            bl_small = pygame.transform.scale(self.tiles[bl[0][0]][bl[0][1]], (size, size))
        elif voisin_8[1][0] == val and voisin_8[2][1] == val and voisin_8[2][0] != val:
            bl_small = pygame.transform.scale(self.tiles[bl[1][0]][bl[1][1]], (size, size))
        elif voisin_8[1][0] != val and voisin_8[2][1] == val:
            bl_small = pygame.transform.scale(self.tiles[bl[2][0]][bl[2][1]], (size, size))
        elif voisin_8[1][0] == val and voisin_8[2][1] != val:
            bl_small = pygame.transform.scale(self.tiles[bl[3][0]][bl[3][1]], (size, size))

        if voisin_8[1][2] != val and voisin_8[0][1] != val:
            tr_small = pygame.transform.scale(self.tiles[tr[0][0]][tr[0][1]], (size, size))
        elif voisin_8[1][2] == val and voisin_8[0][1] == val and voisin_8[0][2] != val:
            tr_small = pygame.transform.scale(self.tiles[tr[1][0]][tr[1][1]], (size, size))
        elif voisin_8[1][2] != val and voisin_8[0][1] == val:
            tr_small = pygame.transform.scale(self.tiles[tr[2][0]][tr[2][1]], (size, size))
        elif voisin_8[1][2] == val and voisin_8[0][1] != val:
            tr_small = pygame.transform.scale(self.tiles[tr[3][0]][tr[3][1]], (size, size))

        if voisin_8[1][2] != val and voisin_8[2][1] != val:
            br_small = pygame.transform.scale(self.tiles[br[0][0]][br[0][1]], (size, size))
        elif voisin_8[1][2] == val and voisin_8[2][1] == val and voisin_8[2][2] != val:
            br_small = pygame.transform.scale(self.tiles[br[1][0]][br[1][1]], (size, size))
        elif voisin_8[1][2] != val and voisin_8[2][1] == val:
            br_small = pygame.transform.scale(self.tiles[br[2][0]][br[2][1]], (size, size))
        elif voisin_8[1][2] == val and voisin_8[2][1] != val:
            br_small = pygame.transform.scale(self.tiles[br[3][0]][br[3][1]], (size, size))

        tile.blit(tl_small, (0, 0))
        tile.blit(tr_small, (8, 0))
        tile.blit(bl_small, (0, 8))
        tile.blit(br_small, (8, 8))
        return tile

    def check_click_algo(self, pos):
        buttons = ["BFS", "DIJKSTRA", "ASTAR"]
        for i, name in enumerate(buttons):
            rect = pygame.Rect(250 + i*110, 10, 100, 30)
            if rect.collidepoint(pos):
                return name
        return None

    def run(self):
        running = True
        while running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.mode == "edit":
                    if pygame.mouse.get_pressed()[0]:
                        x, y = self.get_cell_from_mouse(pygame.mouse.get_pos())
                        selection = self.check_click_terrain(event.pos)
                        selection_algo = self.check_click_algo(event.pos)
                        if selection_algo:
                            self.algo_actif = selection_algo
                        elif selection:
                            self.terrain_actif = selection
                        elif 0 <= x < self.ROWS and 0 <= y < self.COLS:
                            self.grid[x][y] = 0

                    if pygame.mouse.get_pressed()[2]:
                        x, y = self.get_cell_from_mouse(pygame.mouse.get_pos())
                        if 0 <= x < self.ROWS and 0 <= y < self.COLS:
                            self.grid[x][y] = self.terrain_actif["cost"]

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        x, y = self.get_cell_from_mouse(pygame.mouse.get_pos())
                        self.start = (x, y)

                    if event.key == pygame.K_g:
                        x, y = self.get_cell_from_mouse(pygame.mouse.get_pos())
                        self.goal = (x, y)

                    if event.key == pygame.K_SPACE and self.start and self.goal:
                        self.mode = "run"
                        self.reset_visual()
                        self.score = 0
                        self.path_casse = 0
                        self.score_exp = 0
                        self.exp_casse = 0
                        if self.algo_actif == "DIJKSTRA":
                            self.bfs_gen = Dijkstra(self.grid, self.start, self.goal, self.ROWS, self.COLS)
                        elif self.algo_actif == "ASTAR":
                            self.bfs_gen = A_star(self.grid, self.start, self.goal, self.ROWS, self.COLS)
                        else:
                            self.bfs_gen = bfs(self.grid, self.start, self.goal, self.ROWS, self.COLS)

                    if event.key == pygame.K_r:
                        self.mode = "edit"
                        self.reset_visual()
                    """
                    if event.key == pygame.K_m:
                        f = open("test\\BesoinDeCouper.txt", "w")
                        f.write(str(self.start) + "\n")
                        f.write(str(self.goal) + "\n")
                        for i in range(self.ROWS):
                            for j in range(self.COLS):
                                f.write(str(self.grid[i][j]) + " ")
                            f.write("\n")
                    """
            if self.mode == "run" and self.bfs_gen:
                for _ in range(20):
                    try:
                        action, node = next(self.bfs_gen)

                        if action == "Exploration":
                            self.brightness[node] = 1
                            self.score_exp += self.grid[node[0]][node[1]]
                            self.exp_casse += 1

                        elif action == "path":
                            self.path_cells.add(node)
                            self.path_parent[node] = self.parent
                            self.parent = node
                            self.score += self.grid[node[0]][node[1]]
                            self.path_casse += 1

                    except StopIteration:
                        break

            self.screen.fill((0,0,0))

            for x in range(self.ROWS):
                for y in range(self.COLS):
                    rect = pygame.Rect(y*self.CELL_SIZE, x*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)

                    if self.grid[x][y] == 0:
                        tl = ((1, 12), (0, 14), (2, 12), (1, 13))
                        bl = ((3, 12), (1, 11), (2, 12), (3, 13))
                        tr = ((1, 14), (0, 13), (2, 14), (1, 13))
                        br = ((3, 14), (2, 11), (2, 14), (3, 13))
                        tile = self.generate_tiles(x, y, (2, 13), tl, bl, tr, br)

                    else:
                        val = self.grid[x][y]
                        terrain = next(t for t in self.terrains if t["cost"]==val)
                        b = self.brightness[(x,y)]

                        if val == 1:
                            tl = ((5, 4), (4, 7), (6, 4), (5, 5))
                            bl = ((7, 4), (5, 7), (6, 4), (7, 5))
                            tr = ((5, 6), (3, 7), (6, 6), (5, 5))
                            br = ((7, 6), (2, 7), (6, 6), (7, 5))
                            tile = self.generate_tiles(x, y, (6, 5), tl, bl, tr, br)

                        elif val == 3:
                            tl = ((9, 4), (8, 5), (10, 4), (9, 5))
                            bl = ((11, 4), (9, 7), (10, 4), (11, 5))
                            tr = ((9, 6), (8, 6), (10, 6), (9, 5))
                            br = ((11, 6), (8, 7), (10, 6), (11, 5))
                            tile = self.generate_tiles(x, y, (10, 5), tl, bl, tr, br)

                        elif val == 5:
                            tl = ((0, 8), (4, 9), (1, 8), (0, 9))
                            bl = ((2, 8), (3, 9), (1, 8), (2, 9))
                            tr = ((0, 10), (4, 9), (1, 10), (0, 9))
                            br = ((2, 10), (3, 8), (1, 10), (2, 9))
                            tile = self.generate_tiles(x, y, (1, 9), tl, bl, tr, br)

                    self.screen.blit(tile, rect)

                    if self.brightness[(x,y)] > 0:
                        overlay = pygame.Surface((self.CELL_SIZE, self.CELL_SIZE), pygame.SRCALPHA)
                        overlay.fill((255, 255, 255, 50))
                        self.screen.blit(overlay, rect)

                    if (x,y) in self.path_cells and (x, y) != self.start:
                        sprite_path = pygame.transform.rotate(self.way, 0)
                        if self.path_parent[(x, y)] == (x, y-1):
                            sprite_path = pygame.transform.rotate(self.way, 90)
                        elif self.path_parent[(x, y)] == (x-1, y):
                            sprite_path = pygame.transform.rotate(self.way, 0)
                        elif self.path_parent[(x, y)] == (x+1, y):
                            sprite_path = pygame.transform.rotate(self.way, 180)
                        elif self.path_parent[(x, y)] == (x, y+1):
                            sprite_path = pygame.transform.rotate(self.way, -90)
                        self.screen.blit(sprite_path, (rect.x, rect.y))

            if self.start:
                self.screen.blit(self.player_BFS, (self.start[1]*self.CELL_SIZE, self.start[0]*self.CELL_SIZE))

            if self.goal:
                self.screen.blit(self.castle, (self.goal[1]*self.CELL_SIZE, self.goal[0]*self.CELL_SIZE))

            for i, t in enumerate(self.terrains):
                rect = pygame.Rect(10 + i*60, 10, 48, 48)
                sprite_redim = pygame.transform.scale(t["sprite"], (48, 48))
                self.screen.blit(sprite_redim, rect)

                if t == self.terrain_actif:
                    overlay = pygame.Surface((48, 48), pygame.SRCALPHA)
                    overlay.fill((255, 255, 255, 80))
                    self.screen.blit(overlay, (rect.x, rect.y))

            buttons = ["BFS", "DIJKSTRA", "ASTAR"]

            for i, name in enumerate(buttons):
                rect = pygame.Rect(250 + i*110, 10, 100, 30)

                if name == self.algo_actif:
                    pygame.draw.rect(self.screen, (255,255,255), rect)
                    text_color = (0,0,0)
                else:
                    pygame.draw.rect(self.screen, (80,80,80), rect)
                    text_color = (255,255,255)

                text = self.font.render(name, True, text_color)
                self.screen.blit(text, (rect.x + 10, rect.y + 5))

            legend = [
                "Clic gauche = mur",
                "Clic droit = effacer",
                "S = départ | G = objectif",
                "SPACE = lancer BFS",
                "R = reset",
                f"Longueur chemin : {self.path_casse}",
                f"Coût chemin : {self.score}",
                f"Cases explorées : {self.exp_casse}",
                f"Coût exploration : {self.score_exp}"
            ]
            for i, text in enumerate(legend):
                img = self.font.render(text, True, (255,255,255))
                self.screen.blit(img, (10, self.ROWS*self.CELL_SIZE + 5 + i*15))

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()
