FROM jenkins/jenkins:latest

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv \
    git curl build-essential scons pkg-config libx11-dev libxcursor-dev libxinerama-dev libgl1-mesa-dev libglu-dev libasound2-dev libpulse-dev libfreetype6-dev libssl-dev libudev-dev libxi-dev clang netcat-traditional && \
    apt-get clean

RUN python3 -m venv /home/jenkins/xumes_env
RUN /home/jenkins/xumes_env/bin/pip install --upgrade pip setuptools

RUN git clone https://github.com/mastainvin/godot.git /home/jenkins/godot-fork

RUN cd /home/jenkins/godot-fork && \
    git checkout xumes && \
    scons platform=linuxbsd use_llvm=yes -j2


RUN --mount=type=secret,id=github_token \
    git clone https://$(cat /run/secrets/github_token)@github.com/mastainvin/Xumes.git /home/jenkins/xumes


RUN /home/jenkins/xumes_env/bin/pip install --no-cache-dir /home/jenkins/xumes

RUN chown -R jenkins:jenkins /home/jenkins/xumes_env && chmod -R 777 /home/jenkins/xumes_env

RUN jenkins-plugin-cli --plugins "workflow-job workflow-aggregator"

COPY create-job.groovy /usr/share/jenkins/ref/init.groovy.d/

ENV JENKINS_OPTS="--httpPort=80"

EXPOSE 80
EXPOSE 50000

USER jenkins
