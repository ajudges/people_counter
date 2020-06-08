#!/bin/bash

echo "Installing nodejs, modules required for mqtt server and ffmpeg"

# function for linux setup
function install_Nodejs_and_dependencies{
    echo "Nodejs and its dependencies"
    echo "if you have used Chris Lea's Node.js PPA. Enter "1" for yes and "0" for no"
    read Nodejs_hist
    if  [ $Nodejs_hist -eq 1 ] 
    then
    sudo add-apt-repository -y -r ppa:chris-lea/node.js
    sudo rm -f /etc/apt/sources.list.d/chris-lea-node_js-*.list
    sudo rm -f /etc/apt/sources.list.d/chris-lea-node_js-*.list.save
    fi
    curl -sSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | sudo apt-key add -
    VERSION=node_6.x
    DISTRO="$(lsb_release -s -c)"
    echo "deb https://deb.nodesource.com/$VERSION $DISTRO main" | sudo tee /etc/apt/sources.list.d/nodesource.list
    echo "deb-src https://deb.nodesource.com/$VERSION $DISTRO main" | sudo tee -a /etc/apt/sources.list.d/nodesource.list
    sudo apt-get update
    sudo apt-get install nodejs
}

function install_other_dependencies{
    sudo apt update
    sudo apt-get install python3-pip
    pip3 install numpy
    pip3 install paho-mqtt
    sudo apt install libzmq3-dev libkrb5-dev
    sudo apt install ffmpeg
    sudo apt-get install cmake

}

function install_npm{
    sudo npm install npm -g 
    rm -rf node_modules
    npm cache clean
    npm config set registry "http://registry.npmjs.org"
    npm install

}

function install ffmpeg{
npm install ffmpeg
}

# Mac function to install nodejs
function mac_install_nodejs {
    # update brew
    brew update
    brew doctor
    # installing node and npm
    brew install node
    # print the version of node installed
    node -v
    #print the version of npm installed
    npm -v
}

# Mac function to install modules
function mac_install_dep {
    pip3 install numpy
    pip3 install paho-mqtt
    brew install cmake
    brew install zeromq
}

# Mac function to install FFmpeg's ffserver
function mac_install_ff {
    git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
    cd ffmpeg
    git checkout 2ca65fc7b74444edd51d5803a2c1e05a801a6023
    ./configure
    make -j4
}


# obtain  os type
p_name=`uname`
echo $p_name

if [ "$p_name" == 'Linux' ]
then
    echo $(lsb_release -i -s)
    
#   install_Nodejs_and_dependencies
    install_Nodejs_and_dependencies
    
#   install_other_dependencies
    install_other_dependencies
    
#   install_npm
    install_npm
    
#   install ffmpeg
    install ffmpeg
elif [ "$p_name" == 'Darwin']
then
    echo "I am a Mac"
    # Return 1 if python version is ≥ 3.5, otherwise return 0 if python < 3.5 or doesn't exist.
    py_version=$(python -c"import sys; print(0) if sys.version_info.major < 3 and sys.version_info.minor < 5 else print(1)")
    # if python version is ≥ 3.5, do
    if [ $py_version == 1 ]
    then
        # install nodejs
        mac_install_nodejs
        # install dependencies
        mac_install_dep
        # install ffserver
        mac_install_ff

    # if python version is < 3.5 or python isn't installed
    else
        # use brew to install python
        brew install python3
        # install nodejs
        mac_install_nodejs
        # install dependencies
        mac_install_dep
        # install ffserver
        mac_install_ff
    fi
fi    
