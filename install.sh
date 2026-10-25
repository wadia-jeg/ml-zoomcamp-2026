#!/bin/bash

# 1. Uninstall old versions of Docker, if any
# This ensures there are no conflicts with existing installations.
sudo systemctl stop docker
sudo systemctl stop docker.socket
sudo systemctl stop containerd

# Remove Docker Engine, CLI, containerd, and plugins
sudo apt-get purge -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras

# Remove unused dependencies
sudo apt-get autoremove -y --purge

# Remove all Docker data (images, containers, volumes, build cache)
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd

# Remove Docker configuration
sudo rm -rf /etc/docker
sudo rm -f /etc/apt/sources.list.d/docker.sources
sudo rm -f /etc/apt/sources.list.d/docker.list
sudo rm -f /etc/apt/keyrings/docker.asc

# Remove Docker socket
sudo rm -f /var/run/docker.sock

# Remove all Docker data (images, containers, volumes, build cache)
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd

# Remove Docker configuration
sudo rm -rf /etc/docker
sudo rm -f /etc/apt/sources.list.d/docker.sources
sudo rm -f /etc/apt/sources.list.d/docker.list
sudo rm -f /etc/apt/keyrings/docker.asc

# Remove Docker socket
sudo rm -f /var/run/docker.sock

# Remove Docker CLI configuration for your user
rm -rf ~/.docker

which docker
docker --version

# 2. Update the package database
sudo apt-get update

# 3. Download and run the official Docker get script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 4. Add your current user ('vscode') to the docker group so you don't need 'sudo' every time
sudo usermod -aG docker $USER

# 5. Refresh your shell group permissions immediately
newgrp docker

# 6. Start the Docker service daemon
sudo service docker start

rm -r get-docker.sh

docker --version


# 1. Download the latest stable kubectl binary
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# 2. Make it executable
chmod +x kubectl

# 3. Move it to your system path
sudo mv kubectl /usr/local/bin/

# 4. Verify it works
kubectl version --client