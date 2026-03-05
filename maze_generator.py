from pydantic import BaseModel, Field, ValidationError, model_validator
import random

class MazeConfig(BaseModel):
    width: int = Field(..., ge=9)
    height: int = Field(..., ge=6)
    entry: list[int] = Field(..., min_length=2, max_length=2)
    exit: list[int] = Field(..., min_length=2, max_length=2)
    output_file: str = Field(...)
    perfect: bool = Field(...)
    seed: int | None = Field(default=None)

    @model_validator(mode='after')
    def validate_rules(self) -> 'MazeConfig':
        if not (self.entry[0] < self.width and self.entry[0] > 0
            and self.entry[1] < self.height and self.entry[1] > 0):
            raise ValueError("Entry can't is in this place")

        if not (self.exit[0] < self.width and self.exit[0] > 0
            and self.exit[1] < self.height and self.exit[1] > 0):
            raise ValueError("Exit can't is in this place")

        if (".txt" not in self.output_file):
            raise ValueError("output file must be a .txt")

        return self


class MazeGenerator():
    def __init__(self):
        self.maze = {}

        self.config = {}
        mandatory_keys = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT"
        ]
        additional_keys = [
            "SEED"
        ]

        with open("config.txt", "r") as f:
            config_file = f.read().split("\n")


        i = 0
        for line in config_file:
            if line.startswith("#"):
                continue

            if not line.strip():
                continue

            param = line.split("=")
            if ((not param[0] in mandatory_keys)
                and (not param[0] in additional_keys)):
                raise KeyError(f"this key is invalid '{param[0]}'")
            if len(param) != 2:
                raise KeyError("line must be 'key=value'")

            self.config[param[0]] = param[1]

        mandatories = 0
        for key in self.config.keys():
            if key in mandatory_keys:
                mandatories += 1

        if mandatories != len(mandatory_keys):
            raise KeyError("missing a mandatory key")

        validated = MazeConfig(
            width=int(self.config["WIDTH"]),
            height=int(self.config["HEIGHT"]),
            entry=list(map(int, self.config["ENTRY"].split(","))),
            exit=list(map(int, self.config["EXIT"].split(","))),
            output_file=self.config["OUTPUT_FILE"],
            perfect=self.config["PERFECT"].lower() == "true",
            seed=int(self.config["SEED"]) if "SEED" in self.config else None
        )

        self.config["WIDTH"] = validated.width
        self.config["HEIGHT"] = validated.height
        self.config["ENTRY"] = tuple(validated.entry)
        self.config["EXIT"] = tuple(validated.exit)
        self.config["PERFECT"] = validated.perfect

    def init_grid(self):
        for x in range(0, int(self.config['WIDTH']) + 2):
            for y in range(0, int(self.config["HEIGHT"]) + 2):
                self.maze[f"{x}:{y}"] = 1

    def prim(self):
        start_x = 1
        start_y = 1

        self.maze[f"{start_x}:{start_y}"] = 0
        visited = set()
        visited.add((start_x, start_y))
        frontiers = []

        directions = [
        ((start_x, start_y - 1), (start_x, start_y - 2)),
        ((start_x, start_y + 1), (start_x, start_y + 2)),
        ((start_x + 1, start_y), (start_x + 2, start_y)),
        ((start_x - 1, start_y), (start_x - 2, start_y)),
        ]

        for mur, cellule in directions:
            cellx, celly = cellule
            if (0 < cellx < int(self.config['WIDTH']) + 1
                and 0 < celly < int(self.config["HEIGHT"]) + 1):
                frontiers.append(mur)

        while frontiers:
            mur = random.choice(frontiers)
            frontiers.remove(mur)
            murx, mury = mur

            if murx % 2 == 0:
                c1 = (murx - 1, mury)
                c2 = (murx + 1, mury)
            else:
                c1 = (murx, mury - 1)
                c2 = (murx, mury + 1)

            c1_visited = c1 in visited
            c2_visited = c2 in visited
            if c1_visited != c2_visited:
                self.maze[f"{murx}:{mury}"] = 0
                new_cell = c2 if c1_visited else c1
                newx, newy = new_cell
                self.maze[f"{newx}:{newy}"] = 0
                visited.add(new_cell)
                directions = [
                    ((newx, newy - 1), (newx, newy - 2)),
                    ((newx, newy + 1), (newx, newy + 2)),
                    ((newx + 1, newy), (newx + 2, newy)),
                    ((newx - 1, newy), (newx - 2, newy)),
                ]
                for mur, cellule in directions:
                    cellx, celly = cellule
                    if (0 < cellx < int(self.config['WIDTH']) + 1
                        and 0 < celly < int(self.config["HEIGHT"]) + 1):
                        frontiers.append(mur)

    def add_42(self):
        # 4
        self.maze["2:2"] = 1
        self.maze["2:3"] = 1
        self.maze["2:4"] = 1
        self.maze["3:4"] = 1
        self.maze["4:4"] = 1
        self.maze["4:5"] = 1
        self.maze["4:6"] = 1

        # 2
        self.maze["6:2"] = 1
        self.maze["7:2"] = 1
        self.maze["8:2"] = 1
        self.maze["8:3"] = 1
        self.maze["8:4"] = 1
        self.maze["7:4"] = 1
        self.maze["6:4"] = 1
        self.maze["6:5"] = 1
        self.maze["6:6"] = 1
        self.maze["7:6"] = 1
        self.maze["8:6"] = 1


    def fix_isolated(self):
        pass



    def encode_hex(self, x, y):
        north_bit = 0
        east_bit  = 1
        south_bit = 2
        west_bit  = 3

        value = 0
        if self.maze[f"{x}:{y-1}"] == 1:
            value |= 1 << north_bit

        if self.maze[f"{x}:{y+1}"] == 1:
            value |= 1 << south_bit

        if self.maze[f"{x-1}:{y}"] == 1:
            value |= 1 << west_bit

        if self.maze[f"{x+1}:{y}"] == 1:
            value |= 1 << east_bit
        return hex(value)[2:].upper()

    def write_output(self):
        with open(self.config['OUTPUT_FILE'], 'w') as f:
            for y in range(1, int(self.config["HEIGHT"]) + 1):
                row = []
                for x in range(1, int(self.config['WIDTH']) + 1):
                    row.append(self.encode_hex(x, y))
                f.write("".join(row) + "\n")
            entry_x, entry_y = self.config['ENTRY']
            exit_x, exit_y = self.config['EXIT']
            f.write(f"\n{entry_x},{entry_y}\n")
            f.write(f"{exit_x},{exit_y}\n")
