import random
import socket
import json


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


host = '127.0.0.1'
sport = 8080

# Connect to the server -> GAME ENGINE SERVER
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, sport))
    data = {
        "command": "start_scenario",
        "name": "PipeHeightStage",
    }
    s.send(json.dumps(data).encode())

    data = s.recv(1024)
    data = data.decode()
    data = json.loads(data)
    data = parse_json_with_eval(data)

    port = data["port"]

    # Connect to server -> SCENE INSTANCE SERVER
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
        print(port)
        s2.connect((host, port))
        try:
            data = {
                "args": {
                    "when": {
                        "speed": 0,
                        "position": {
                            "x": 0,
                            "y": 0
                        }
                    },
                },
            }

            s2.send(json.dumps(data).encode())

            while True:
                data = s2.recv(1024, ).decode()
                data = json.loads(data)
                data = parse_json_with_eval(data)
                print(data)

                # do_jump one time out of 100
                do_jump = random.randint(0, 50) == 0

                if do_jump:
                    event = {
                        "inputs": [
                            {"type": "JOY_BUTTON_EVENT", "button": "A"},
                        ],
                    }
                else:
                    event = {
                        "inputs": [
                        ],
                    }

                s2.send(json.dumps(event).encode())

        except:
            print("Server shutting down")
            if s:
                s.close()
            if s2:
                s2.close()
