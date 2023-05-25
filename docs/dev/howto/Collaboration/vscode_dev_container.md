# Development container in vs code

## **Summary**

This document describes how to setup a development container for VSCode using Docker. cisTEM can be somewhat complicated to build, and this is a way to ensure that everyone is building in the same environment. This is also a way to ensure that the build environment is consistent across platforms.

We will cover:
- Installing prerequisites
- Building the development container
- Using the development container

We will not cover:
- altering or extending the development container

## **Prerequisites**

- ***vscode***
    - *w/ dev containers extension*
- ***docker***
    - optional: *nvidia-docker*
- ***cisTEM source code***

```{note} 
* This document assumes that you either have already installed vscode and docker, or are able to install them which requires sudo.

* The following instructions are for reference to how I setup these prerequisites on Ubuntu 20.04. 
    - *Please refer to the official documentation for your platform.*
```



### Install vscode [(official docs)](https://code.visualstudio.com/docs/setup/linux)

```bash
sudo apt install software-properties-common apt-transport-https wget
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
sudo apt install code
```

### Install Docker [(official docs)](https://docs.docker.com/engine/install/ubuntu/)

```bash
# FIRST, cleanup any old install if you have one (or just use your existing install)
sudo apt remove docker-desktop
rm -r $HOME/.docker/desktop
sudo rm /usr/local/bin/com.docker.cli
sudo apt purge docker-desktop

# SECOND install

sudo apt-get update
sudo apt-get install curl
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo docker run hello-world
sudo usermod -aG docker ${USER}
chmod 664 /var/run/docker.sock
# log out log back in
```

```{admonition} gpu code in the dev container
:class: dropdown
If you want to run any gpu code ***inside*** the dev container, you will need to [install nvidia-docker](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker).

The binaries you compile with the default dev container will run ***outside*** the dev container without nvidia-docker assuming you have a compatible gpu driver installed.
```


### Install the cisTEM source code

```bash
git clone git@github.com:timothygrant80/cisTEM.git
```

## **Building the development container**

From the cisTEM source code directory, run the following command:

```bash
ln -s .vscode_shared/CistemDev .vscode
ln -s .vscode/devcontainer_wxStable_static.json .devcontainer.json
code .
```

```{admonition} dev container extension

If you installed vscode fresh following the instructions above, or if you do not have the **dev containers** vscode extension, install this from the extensions marketplace.
```

Assuming you properly created the links when setting up the source code directory, you should be able to build the devcontainer in several ways.

The easiest is to type **ctrl+shift+p** and type **Reopen in Container**. This will build the container and open the source code directory in the container.

Depending on your internet connection, this may take a little while as the docker images (~12 Gb) are downloaded and built.


## **Using the development container**

- Setup autotools

```bash
./regenerate_project.b
```

- Configure the type of build you want for cisTEM.
    - **ctrl+shift+p** and type **Tasks: Run Task**
    - Select **Configure cisTEM build**

- Build cisTEM
    - **ctrl+shift+p** and type **Tasks: Run Task**
    - Select **Build cisTEM**

