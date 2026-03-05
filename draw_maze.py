from draw_path import calcul_path_coordinates, find_path
from maze_generator import MazeGenerator
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


def print_walls(cell_walls, width, cell, screen, x, y, x1, y1, x2, y2, color_ft):
    for i, dic in enumerate(cell_walls):
            x0 = i % width
            y0 = i // width
            cell_x = x + x0 * cell
            cell_y = y + y0 * cell
            cellx_i = x + x1 * cell
            celly_i = y + y1 * cell
            if cell_x == cellx_i and cell_y == celly_i:
                pygame.draw.rect(screen,
                                 (0, 255, 0),
                                 (cellx_i, celly_i, cell, cell))
            cellx_o = x + x2 * cell
            celly_o = y + y2 * cell
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
            for coordinate in color_ft:
                xc, yc = coordinate
                cell_xft = x + xc * cell
                cell_yft = y + yc * cell
                if cell_x == cell_xft and cell_y == cell_yft:
                    pygame.draw.rect(screen,
                                     (0, 0, 255),
                                     (cell_x, cell_y, cell, cell))


def print_path(cell_walls, width, cell, screen, x, y, x1, y1, x2, y2, color_ft, path_coordinates):
    print_walls(cell_walls, width, cell, screen, x, y, x1, y1, x2, y2, color_ft)
    for i, dic in enumerate(cell_walls):
        x0 = i % width
        y0 = i // width
        cell_x = x + x0 * cell
        cell_y = y + y0 * cell
        for coordinate in path_coordinates:
            xc, yc = coordinate
            cell_xft = x + xc * cell
            cell_yft = y + yc * cell
            if cell_x == cell_xft and cell_y == cell_yft:
                pygame.draw.rect(screen,
                                (0, 255, 0),
                                (cell_x, cell_y, cell, cell))


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
    color_ft = [(2, 2), (2, 3), (2, 4), (3, 4),
                (4, 4), (4, 5), (4, 6), (6, 2),
                (7, 2), (8, 2), (8, 3), (8, 4),
                (7, 4), (6, 4), (6, 5), (6, 6), (7, 6), (8, 6)]
    cell_walls = run_maze(hexas, width, height)
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((width*50, height*50))
    x = 0
    y = 0
    pygame.display.set_caption("A_maze_ing")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont('monospace', 23)
    lignes = ["=== A_Maze_Ing ===",
              "1- Re-generate a new maze",
              "2- Show path from entry to exit",
              "3- Rotate maze colors",
              "4- Quit"]
    surf1 = pygame.Rect(0, (height+3)*cell + 32, 350, 30)
    surf2 = pygame.Rect(0, (height+3)*cell + 32*2, 500, 30)
    surf3 = pygame.Rect(0, (height+3)*cell + 32*3, 300, 30)
    surf4 = pygame.Rect(0, (height+3)*cell + 32*4, 100, 30)
    surf5 = pygame.Rect(60, (height+3)*cell, 140, 20)
    wav_sound = pygame.mixer.Sound("sound.wav")
    wav_sound.set_volume(0.5)
    path = find_path(maze_datas)
    path_coordinates = calcul_path_coordinates(inp, path)
    show_path = False
    path = lignes[2].replace("Show", "Hide") if show_path else lignes[2]
    while True:
        mouse_pos = pygame.mouse.get_pos()
        if surf1.collidepoint(mouse_pos) or surf2.collidepoint(mouse_pos)\
        or surf3.collidepoint(mouse_pos) or surf4.collidepoint(mouse_pos)\
        or surf5.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if surf1.collidepoint(mouse_pos):
                        wav_sound.play()
                        maze = MazeGenerator()
                        maze.init_grid()
                        maze.prim()
                        maze.add_42()
                        maze.fix_isolated()
                        maze.write_output()
                        draw_maze(maze.config)
                    elif surf2.collidepoint(mouse_pos):
                        wav_sound.play()
                        if show_path is False:
                            print_path(cell_walls, width, cell, screen, x, y, x1, y1, x2, y2, color_ft, path_coordinates)
                            show_path = not show_path
                        else:
                            print_walls(cell_walls, width, cell, screen, x, y, x1, y1, x2, y2, color_ft)
                            show_path = not show_path
                    elif surf3.collidepoint(mouse_pos):
                        wav_sound.play()
                    elif surf4.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    elif surf5.collidepoint(mouse_pos):
                        sound = pygame.mixer.Sound("amongus.wav")
                        sound.set_volume(3.0)
                        sound.play()

        pygame.draw.rect(screen,
                         (255, 255, 255),
                         (x, y, (width+2) * cell, (height+2) * cell), cell)
        print_walls(cell_walls, width, cell, screen, x, y, x1, y1, x2, y2, color_ft)
        for i, ligne in enumerate(lignes):
            surf = font.render(ligne, True, (255, 255, 255))
            screen.blit(surf, (1, (height+3)*cell + i * 35))
        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    draw_maze()
