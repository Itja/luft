#!/bin/bash
git pull
sudo python3 -m pip uninstall Homie4
git clone --branch fix/mqtt-disconnect-property https://github.com/Itja/Homie4.git ../Homie4
ln -s ../Homie4/homie ./homie
sudo ./install-system-ctl.sh
