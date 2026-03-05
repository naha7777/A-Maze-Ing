from enum import Enum


class Walls(Enum):
    S = ":---"
    N = ":---"
    E = "|"
    W = "|   "


class MazeGenerator:
    def __init__(self, height: int, width: int, entry: tuple, exit: tuple):
        self.height = height
        self.width = width
        self.entry = entry
        self.exit = exit
        self.NORTH = ["1", "3", "5", "7", "9", "B", "D", "F"]
        self.SOUTH = ["4", "5", "6", "7", "C", "D", "E", "F"]
        self.EST = ["2", "3", "6", "7", "A", "B", "E", "F"]
        self.WEST = ["8", "9", "A", "B", "C", "D", "E", "F"]

    def run_maze(self, hexa: str) -> dict:
        all_coordinates = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                coordinates = (y, x)
                all_coordinates.append(coordinates)
        hexa_coordinates = {}
        i = 0
        for c in hexa:
            if not c or c == "\n":
                continue
            walls = {"N": 0, "S": 0, "E": 0, "W": 0}
            if c in self.NORTH:
                walls["N"] = 1
            if c in self.SOUTH:
                walls["S"] = 1
            if c in self.EST:
                walls["E"] = 1
            if c in self.WEST:
                walls["W"] = 1
            hexa_coordinates[all_coordinates[i]] = walls
            if i < len(all_coordinates) - 1:
                i += 1
        return hexa_coordinates

    def print_maze(self, directions: dict) -> None:
        for y in range(0, self.height):
            top = ""
            mid = ""
            botom = ""
            for x in range(self.width):
                cell = directions.get((y, x), {})
                n = cell.get("N", 0)
                s = cell.get("S", 0)
                w = cell.get("W", 0)
                if x != self.width - 1:
                    top += Walls.N.value if n else "    "
                else:
                    top += ":---:"
                mid += Walls.W.value if w else "    "
                if x == self.width - 1:
                    mid += Walls.E.value
                botom += Walls.S.value if s else "    "
            if ":--- " in top:
                top = top.replace(":--- ", ":---:")
            if top.startswith(":"):
                print(f"{top}\n{mid}")
        botom.replace("::", ":")
        print(f"{botom}:")


def maze_gen_ascii(config: dict) -> None:
    generator = MazeGenerator(config.get("HEIGHT"),
                              config.get("WIDTH"),
                              config.get("ENTRY"),
                              config.get("EXIT"))
    with open("maze.txt", "r") as file:
        hexa = file.read()
    directions_coordinates = generator.run_maze(hexa)
    generator.print_maze(directions_coordinates)


if __name__ == "__main__":
    maze_gen_ascii()
