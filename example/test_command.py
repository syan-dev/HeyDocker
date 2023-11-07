import logging
import sys

from heydocker.functions.gpt import GPTClient

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

if __name__ == "__main__":
    # get message from user argument
    message = sys.argv[1]

    # create GPT client
    gpt_client = GPTClient()
    print(gpt_client.handle_command(message))
