import game_bfs
import load_env

if __name__ == "__main__":
    grid, star, goal = load_env.loadEnv("test\\Montagne.txt")
    game = game_bfs.Game()
    game.start = star
    game.goal = goal
    game.grid = grid
    game.run()