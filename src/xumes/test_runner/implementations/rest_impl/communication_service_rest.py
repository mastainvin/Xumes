import requests


class CommunicationServiceRest:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start_scenario(self, name: str) -> int:

        port = 0
        # call the REST API to get the port
        http_response = requests.get(f"http://{self.host}:{self.port}/start_scenario/{name}")
        if http_response.status_code == 200:
            port = http_response.json()
            print(http_response, port)
        return port
