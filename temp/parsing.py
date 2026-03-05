def check_config(mandatory: list, config: dict) -> dict:
    valid_config = {}
    for k, v in config.items():
        if k == mandatory[0]:
            v = int(v)
            if v < 0:
                raise ValueError("ERROR: WIDTH must be positive")
        elif k == mandatory[1]:
            v = int(v)
            if v < 0:
                raise ValueError("ERROR: HEIGHT must be positive")
        elif k == mandatory[2]:
            split_v = v.split(",")
            if len(split_v) != 2:
                raise ValueError("ERROR: coordinates need two integers")
            split_v[0] = int(split_v[0])
            split_v[1] = int(split_v[1])
            if split_v[0] < 0 or split_v[1] < 0\
                or split_v[0] >= valid_config.get("WIDTH")\
                    or split_v[1] > valid_config.get("HEIGHT") - 1:
                raise ValueError("ERROR: ENTRY need positives coordinates")
            v = (split_v[0], split_v[1])
        elif k == mandatory[3]:
            split_v = v.split(",")
            split_v[0] = int(split_v[0])
            split_v[1] = int(split_v[1])
            if split_v[0] < 0 or split_v[1] < 0\
                or split_v[0] >= valid_config.get("WIDTH")\
                    or split_v[1] > valid_config.get("HEIGHT") - 1:
                raise ValueError("ERROR: EXIT need positives coordinates")
            v = (split_v[0], split_v[1])
        elif k == mandatory[4]:
            if v != "maze.txt":
                raise ValueError("ERROR: OUTPUT_FILE expect maze.txt")
        elif k == mandatory[5]:
            if v not in ("True", "False"):
                raise ValueError("ERROR: PERFECT expect a boolean")
            v = v == "True"
        valid_config[k] = v
    if valid_config.get("ENTRY") == valid_config.get("EXIT"):
        raise ValueError("ERROR: ENTRY and EXIT can't have the same"
                         " coordinates")
    return valid_config


def parsing() -> dict:
    mandatory_keys = ["WIDTH",
                      "HEIGHT",
                      "ENTRY",
                      "EXIT",
                      "OUTPUT_FILE",
                      "PERFECT"]
    config_dict = {}
    with open("config.txt", "r") as config_file:
        config_data = config_file.read()
    lines = config_data.split("\n")
    if "WIDTH" not in config_data\
        or "HEIGHT" not in config_data\
        or "ENTRY" not in config_data\
        or "EXIT" not in config_data\
        or "OUTPUT_FILE" not in config_data\
            or "PERFECT" not in config_data:
        print("ERROR: A key is missing")
        exit(1)
    for line in lines:
        if line.startswith("#") or not line:
            for key in mandatory_keys:
                if key in line:
                    print("ERROR: A key is missing")
                    exit(1)
            continue
        if line is None:
            continue
        key_value = line.split("=")
        if key_value[0] in mandatory_keys:
            config_dict[key_value[0]] = key_value[1]
        else:
            print("ERROR config.txt")
            exit(1)
    try:
        valid = check_config(mandatory=mandatory_keys, config=config_dict)
    except ValueError as e:
        print(e)
        exit(1)
    return valid


if __name__ == "__main__":
    parsing()
