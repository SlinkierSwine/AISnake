import configparser
import os


def create_config(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("GAME")
    config.add_section("NN")
    config.set("GAME", "FPS", "120")
    config.set("GAME", "CELL_SIZE", "30")
    config.set("GAME", "WIDTH", "20")
    config.set("GAME", "HEIGHT", "20")
    config.set("NN", "GENERATIONS", "50")

    with open(path, "w") as config_file:
        config.write(config_file)


def read_config(path):
    config = configparser.ConfigParser()
    if not os.path.exists(path):
        create_config(path)
    config.read(path)
    return config


if __name__ == "__main__":
    path = "config.cfg"
    create_config(path)
