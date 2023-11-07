import configparser
import os


def get_telegram_token():
    token = os.environ.get("TELEGRAM_TOKEN")
    # if environ var empty, check ~/.heydocker/credentials
    if token is None and os.path.exists(os.path.expanduser("~/.heydocker/credentials")):
        config = configparser.ConfigParser()
        config.read(os.path.expanduser("~/.heydocker/credentials"))
        token = config["telegram"]["token"]

    return token


def get_telegram_allowed_ids():
    allowed_ids = os.environ.get("TELEGRAM_ALLOWED_IDS")
    # if environ var empty, check ~/.heydocker/credentials
    if allowed_ids is None and os.path.exists(
        os.path.expanduser("~/.heydocker/credentials")
    ):
        config = configparser.ConfigParser()
        config.read(os.path.expanduser("~/.heydocker/credentials"))
        allowed_ids = config["telegram"]["allowed_ids"]

    allowed_ids = allowed_ids.split(",")
    print(allowed_ids)
    print(type(allowed_ids))
    print("...")
    return [int(x) for x in allowed_ids]


def get_openai_endpoint():
    endpoint = os.environ.get("OPENAI_ENDPOINT")
    # if environ var empty, check ~/.heydocker/credentials
    if endpoint is None and os.path.exists(
        os.path.expanduser("~/.heydocker/credentials")
    ):
        config = configparser.ConfigParser()
        config.read(os.path.expanduser("~/.heydocker/credentials"))
        endpoint = config["openai"]["endpoint"]
    return endpoint


def get_openai_api_key():
    key = os.environ.get("OPENAI_KEY")
    # if environ var empty, check ~/.heydocker/credentials
    if key is None and os.path.exists(os.path.expanduser("~/.heydocker/credentials")):
        config = configparser.ConfigParser()
        config.read(os.path.expanduser("~/.heydocker/credentials"))
        key = config["openai"]["api_key"]
    return key
