#!/bin/bash

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
fi    
