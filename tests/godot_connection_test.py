import socket
import json

# Create a socket object
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind socket to address and port
serverSocket.bind(('127.0.0.1', 12345))

# Listen for incoming connections
serverSocket.listen(5)

print("Server listening on port 12345")


def parse_json_with_eval(json_obj):
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            json_obj[key] = parse_json_with_eval(value)
        return json_obj
    elif isinstance(json_obj, list):
        return [parse_json_with_eval(item) for item in json_obj]
    elif isinstance(json_obj, str):
        try:
            return eval(json_obj)
        except (SyntaxError, NameError, TypeError):
            # Si l'évaluation échoue, on laisse la valeur inchangée
            return json_obj
    else:
        return json_obj


try:

    # Accept connection from client
    clientSocket, address = serverSocket.accept()
    print(f"Connection from {address} has been established.")

    while True:
        data = clientSocket.recv(1024).decode()
        data = json.loads(data)
        data = parse_json_with_eval(data)
        print(data)

        clientSocket.send('{"test": 1}'.encode())
except KeyboardInterrupt:
    print("Server shutting down")
    if clientSocket:
        clientSocket.close()
    if serverSocket:
        serverSocket.close()
