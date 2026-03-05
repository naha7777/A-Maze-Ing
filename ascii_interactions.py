from maze_generator import MazeGenerator
from draw_ascii import draw_ascii

def interactions(maze: MazeGenerator):
    show_path = False
    while True:
        print("\n=== A-maze-ing ===")
        path = "Hide" if show_path else "Show path from entry to exit"
        print("1- Re-generate a new maze")
        print(f"2- {path}")
        print("3- Rotate maze colors")
        print("4- Quit")
        choice = input("Choice (1-4): ")
        try:
            if int(choice) == 1:
                maze.init_grid()
                maze.prim()
                maze.add_42()
                maze.fix_isolated()
                maze.write_output()
                draw_ascii(maze.config)
            elif int(choice) == 2:
                if show_path is False:
                    # appeler la fonction qui montrera le path
                    show_path = not show_path
                else:
                    # rapeler la fonction sans le path
                    show_path = not show_path
            elif int(choice) == 3:
                # color_list = ["rgb.BLUE",
                #               "rgb.YELLOW",
                #               "rgb.PINK",
                #               "rgb,PURPLE",
                #               "rgb.BROWN",
                #               "rgb.GOLD",
                #               "rgb.GRAY",
                #               "rgb.WHITE"]
                # i = 0
                # appeler la fonction avec ou sans path avec en param la couleur
                # a chaque appel on incremente color_list[i] pour avoir une autre couleur
                pass
            elif int(choice) == 4:
                exit(1)
            else:
                print("ERROR: please put 1, 2, 3 or 4 !")
                exit(1)
        except ValueError as e:
            print(e)
            exit(1)


if __name__ == "__main__":
    interactions()
