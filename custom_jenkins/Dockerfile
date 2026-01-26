FROM jenkins/jenkins:lts

USER root

ENV DEBIAN_FRONTEND=noninteractive

RUN set -eux; \
    apt-get update -y; \
    apt-get install -y --no-install-recommends \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release \
        software-properties-common \
        sudo; \
    \
    ARCH="$(dpkg --print-architecture)"; \
    OS_VERSION="$(lsb_release -cs)"; \
    \
    install -m 0755 -d /etc/apt/keyrings; \
    curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc; \
    chmod a+r /etc/apt/keyrings/docker.asc; \
    \
    echo "deb [arch=$ARCH signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $OS_VERSION stable" \
        > /etc/apt/sources.list.d/docker.list; \
    \
    apt-get update -y; \
    apt-get install -y --no-install-recommends \
        docker-ce \
        docker-ce-cli \
        containerd.io \
        docker-buildx-plugin \
        docker-compose-plugin; \
    \
    docker --version; \
    \
    groupadd -f docker; \
    usermod -aG docker jenkins; \
    \
    mkdir -p /var/lib/docker /var/run; \
    chmod 755 /var/lib/docker; \
    \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
        > /etc/apt/sources.list.d/google-cloud-sdk.list; \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -; \
    \
    apt-get update -y; \
    apt-get install -y google-cloud-sdk; \
    \
    gcloud --version; \
    \
    apt-get autoremove -y; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

VOLUME /var/lib/docker

EXPOSE 8080 50000

USER jenkins

WORKDIR /var/jenkins_home