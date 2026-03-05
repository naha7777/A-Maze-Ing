from draw_ascii import draw_ascii
# from draw_maze import draw_maze
from ascii_interactions import interactions
# from draw_path import draw_path
from maze_generator import MazeGenerator
import pydantic


def a_maze_ing():
    # res_parsing = parsing()
    # try:
    #     if "pygame" in res_parsing:
    #         draw_maze(res_parsing)
    #     else:
    #         # draw_ascii(res_parsing)
    #         draw_path(res_parsing)
    #         interactions()
    # except KeyboardInterrupt:
    #     print("\nKO")
    #     exit(1)

    try:
        maze = MazeGenerator()
        maze.init_grid()
        maze.prim()
        maze.write_output()
        draw_ascii(maze.config, "rgb.WHITE")
        interactions(maze)

    except pydantic.ValidationError as e:
        for error in e.errors():
            print(f"ERROR: {error['msg'].replace('Value error, ', '')}")

    except KeyError as e:
        print(f"ERROR: {e}")

    except KeyboardInterrupt:
        print("\nKO")
        exit(1)

if __name__ == "__main__":
    a_maze_ing()
