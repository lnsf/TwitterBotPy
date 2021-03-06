import os
import toml
from botkun import default_config_path
from typing import Dict, Union


class BotConfig:
    def __init__(self,
                 consumer_key: str,
                 consumer_secret: str,
                 access_token: str,
                 access_secret: str,
                 database_path="",
                 twitter_user_name="",
                 ):
        if database_path == "":
            self.database_path = get_library_root_path() + "/database"
        else:
            self.database_path = database_path

        self.twitter_user_name = twitter_user_name
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret = access_secret

        self.local = False
        self.use_database = True
        self.file_path = ""

    def __str__(self) -> str:
        return "consumer_key: " + self.consumer_key + "\n" + \
               "consumer_secret: " + self.consumer_secret + "\n" + \
               "access_token: " + self.access_token + "\n" + \
               "access_secret: " + self.access_secret + "\n" + \
               "user_name: " + self.twitter_user_name + "\n" + \
               "database: " + self.database_path

    def save_arguments(self, options: Dict[str, Union[str, bool]]):
        self.local = options["local"]
        self.use_database = options["database"]
        self.file_path = get_config_file_path(options["config"])


def get_library_root_path() -> str:
    path_to_config_py = os.path.dirname(__file__)  # /path/to/library_root/botkun
    library_root_path = path_to_config_py.replace("/botkun", "")  # /path/to/library_root
    return library_root_path


def get_config_file_path(custom_path_to_config="") -> str:
    path_to_config = custom_path_to_config
    if path_to_config == "":
        exists = [p for p in default_config_path if os.path.isfile(p)]
        if len(exists) == 0:
            print("Config file not found")
            exit(-2)
        else:
            path_to_config = exists[0]

    return path_to_config


def read_config_file(custom_path_to_config="") -> str:
    path_to_config = get_config_file_path(custom_path_to_config)
    try:
        config_file = open(path_to_config, "r")
        config_toml = config_file.read()
        config_file.close()

        return config_toml
    except FileNotFoundError:
        print("Config file not found")
        exit(-2)


def parse_config(config_toml: str) -> BotConfig:
    parsed_config = toml.loads(config_toml)

    return BotConfig(
        consumer_key=parsed_config["api"]["consumer_key"],
        consumer_secret=parsed_config["api"]["consumer_secret"],
        access_token=parsed_config["api"]["access_token"],
        access_secret=parsed_config["api"]["access_secret"],
        twitter_user_name=parsed_config["options"]["twitter_user_name"],
        database_path=parsed_config["options"]["database_path"]
    )


def get_config(custom_path_to_config="") -> BotConfig:
    config_toml = read_config_file(custom_path_to_config)
    return parse_config(config_toml)
