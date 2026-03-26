def loadEnv(path):
    with open(path, 'r') as f:
        lignes = f.readlines()  # Retourne une liste
    s = lignes[0].split(", ")
    star = (int(s[0][1:]), int(s[1][:-2]))
    g = lignes[1].split(", ")
    goal = (int(g[0][1:]), int(g[1][:-2]))

    grid = []
    for i in range(2, len(lignes)):
        grid.append([int(l) for l in lignes[i][:-2].split(" ")])
    return grid, star, goal