#!/bin/bash

# Démarrer le serveur SSH
service ssh start

# Démarrer Godot avec un affichage graphique
Xvfb :0 -screen 0 1024x768x16 &
export DISPLAY=:0
/opt/godot-fork/bin/godot.linuxbsd.editor.x86_64.llvm --path /opt/xumes &

# Garder le conteneur en marche
tail -f /dev/null
