import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

try:
    import pygame
except ModuleNotFoundError:
    print("ERROR: can't use pygame")
    exit(1)


def run_maze(hexa: str, w : int, h: int) -> dict:
    north = ["1", "3", "5", "7", "9", "B", "D", "F"]
    south = ["4", "5", "6", "7", "C", "D", "E", "F"]
    est = ["2", "3", "6", "7", "A", "B", "E", "F"]
    west = ["8", "9", "A", "B", "C", "D", "E", "F"]
    cell_walls = []
    for c in hexa:
        if len(cell_walls) >= w * h:
            break
        if not c or c == "\n":
            continue
        if c not in "0123456789ABCDEF":
            break
        walls = {"N": 0, "S": 0, "E": 0, "W": 0}
        if c in north:
            walls["N"] = 1
        if c in south:
            walls["S"] = 1
        if c in est:
            walls["E"] = 1
        if c in west:
            walls["W"] = 1
        cell_walls.append(walls)
    return cell_walls


def draw_maze(maze_datas: dict) -> None:
    with open("maze.txt", "r") as hexa:
        hexas = hexa.read()
    fps = 60
    inp = maze_datas.get("ENTRY")
    x1, y1 = inp
    outp = maze_datas.get("EXIT")
    x2, y2 = outp
    width = maze_datas.get("WIDTH")
    height = maze_datas.get("HEIGHT")
    cell = 20
    x = 200
    y = 0
    cell_walls = run_maze(hexas, width, height)
    pygame.init()
    screen = pygame.display.set_mode((width*50, height*50))

    pygame.display.set_caption("A_maze_ing")
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (x, y, (width+2) * cell, (height+2) * cell), cell)
        for i, dic in enumerate(cell_walls):
            x0 = i % width
            y0 = i // width
            cellx_i = x + x1 * cell
            celly_i = y + y1 * cell
            cellx_o = x + x2 * cell
            celly_o = y + y2 * cell
            cell_x = x + x0 * cell
            cell_y = y + y0 * cell
            if cell_x == cellx_i and cell_y == celly_i:
                pygame.draw.rect(screen,
                                 (0, 255, 0),
                                 (cellx_i, celly_i, cell, cell))
            if cell_x == cellx_o and cell_y == celly_o:
                pygame.draw.rect(screen,
                                 (255, 0, 0),
                                 (cellx_o, celly_o, cell, cell))
            if dic.get("W") == 1:
                pygame.draw.rect(screen,
                                 (255, 255, 255),
                                 (cell_x, cell_y+20, cell, cell))
            if dic.get("E") == 1:
                pygame.draw.rect(screen,
                                 (255, 255, 255),
                                 (cell_x+40, cell_y+20, cell, cell))
        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    draw_maze()
