FROM ubuntu:20.04

USER root

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Paris

# Installer les paquets nécessaires
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv \
    git curl build-essential scons pkg-config libx11-dev libxcursor-dev libxinerama-dev libgl1-mesa-dev \
    libglu-dev libasound2-dev libpulse-dev libfreetype6-dev libssl-dev libudev-dev libxi-dev clang \
    netcat-traditional openssh-server x11-xserver-utils xvfb libfontconfig1 libxkbcommon0 && \
    apt-get clean

# Configurer l'environnement virtuel Python
RUN python3 -m venv /opt/xumes_env
RUN /opt/xumes_env/bin/pip install --upgrade pip setuptools

# Cloner et compiler Godot
RUN git clone https://github.com/mastainvin/godot.git /opt/godot-fork
RUN cd /opt/godot-fork && \
    git checkout xumes && \
    scons platform=linuxbsd use_llvm=yes -j2

# Installer votre projet
RUN mkdir -p /opt/xumes
COPY ../../ /opt/xumes/
RUN ls -la /opt/xumes
RUN /opt/xumes_env/bin/pip install --no-cache-dir /opt/xumes

# Configuration des permissions
RUN chown -R root:root /opt/xumes_env && chmod -R 777 /opt/xumes_env

# Configurer le serveur SSH
RUN apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Exposer les ports nécessaires
EXPOSE 22

# Script d'entrée pour démarrer Godot et SSH
COPY ./docker/demo/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# xhost +local:root