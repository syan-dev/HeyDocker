import os
import json
from socketserver import UnixStreamServer, BaseRequestHandler
import configparser

from heydocker.database import Database


# check if database directory exists
if not os.path.exists(os.path.expanduser("~/.heydocker")):
    os.makedirs(os.path.expanduser("~/.heydocker"))
database = Database(os.path.expanduser("~/.heydocker/heydocker.db"))


class HTTPMessageBody:
    def __init__(self, message):
        self.message = message


def write_config_file(config_file_path, config_json):
    config = configparser.ConfigParser()
    # check if dir of config file exists
    if not os.path.exists(os.path.dirname(config_file_path)):
        os.mkdir(os.path.dirname(config_file_path))
    
    config["telegram"] = {}
    if config_json.get("token") is not None:
        config["telegram"]["token"] = config_json.get("token")
    if config_json.get("allowed_ids") is not None:
        config["telegram"]["allowed_ids"] = config_json.get("allowed_ids")
    config["openai"] = {}
    if config_json.get("openai_api_key") is not None:
        config["openai"]["api_key"] = config_json.get("openai_api_key")
    with open(config_file_path, "w") as configfile:
        config.write(configfile)


class HelloRequestHandler(BaseRequestHandler):
    def handle(self):
        try:
            data = self.request.recv(1024)  # Receive data from the client
            if data:
                print(data)
                received_data = data.decode()
                print("received_data:", received_data)
                received_method = received_data.split(" ")[0]
                print("received_method:", received_method)
                received_path = received_data.split(" ")[1]
                print("received_path:", received_path)

                if received_method == 'POST':
                    received_message = received_data.split("\r\n\r\n")[1]
                    print("received_message:", received_message)
                    received_message = json.loads(received_message)
                    print("received_message:", received_message)

                    if received_path == "/credentials":
                        write_config_file("/root/.heydocker/credentials", received_message)
                        response = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"status\": \"success\"}"
                        self.request.sendall(response)
                
                elif received_path == "/messages":
                    all_messages = {
                        'messages': database.get()
                    }
                    response = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n" + json.dumps(all_messages).encode()
                    self.request.sendall(response)

        except Exception as e:
            print("Error processing request:", e)

def main():
    socket_path = "/run/guest-services/backend.sock"
    if os.path.exists(socket_path):
        os.remove(socket_path)

    # create repository if not exist
    if not os.path.exists("/run/guest-services"):
        os.mkdir("/run/guest-services")

    print("Starting listening on", socket_path)

    try:
        with UnixStreamServer(socket_path, HelloRequestHandler) as server:
            server.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
