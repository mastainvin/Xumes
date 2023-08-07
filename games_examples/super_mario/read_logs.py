import json
import os

# Ouvrir le fichier JSON en mode lecture ('r')
dir = os.getcwd()
dir_logs = os.path.join(dir, "games_examples", "super_mario", "testing", "game_side", "_logs", "jump", "Jump 150:100")
logs_file = os.path.join(dir_logs, "_logs.json")
print(logs_file)

with open(logs_file, "r") as file:
    data = json.load(file)
    for element in data['jump_step']:
        for dict in element:
            if dict["player"]["position"]["x"] > 224:
                print("Il y a au moins un moment où Mario passe le premier tuyeau")
    print("Il ne passe jamais le premier tuyeau")







# Maintenant, 'data' est un dictionnaire Python contenant les données du fichier JSON
#print(data)
