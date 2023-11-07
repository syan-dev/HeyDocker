from heydocker.functions.gpt import GPTClient

gpt_client = GPTClient()


def run(message: str):
    return gpt_client.handle_command(message)
