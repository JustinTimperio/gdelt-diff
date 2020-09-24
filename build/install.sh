#!/usr/bin/env bash
osname=$(cat /etc/*release | grep -Pi '^ID=' | head -1 | cut -c4- | sed -e 's/^"//' -e 's/"$//')

## DEBIAN
if [[ $osname == 'ubuntu' ]] || [[ $osname == 'debian' ]]; then
  # Install Dependencies
  apt --yes install python3 python3-requests

## CENTOS
elif [[ $osname == 'centos' ]] || [[ $osname == 'fedora' ]]; then
  # Install Dependencies
  yum -y install python38 python38-requests

## ARCH
elif [[ $osname == 'arch' ]] || [[ $osname == 'manjaro' ]]; then
  # Install Dependencies
  pacman -S --noconfirm --needed python python-requests

## NOT SUPPORTED
else
  echo $osname Is Not Supported!
  exit
fi

# Clone Repo
sudo git clone --recurse-submodules https://github.com/JustinTimperio/gdelt-diff.git /opt/gdelt-diff

# Add Config to /etc
sudo mkdir -p /etc/gdelt-diff
sudo cp /opt/gdelt-diff/build/config /etc/gdelt-diff/config
sudo ln -sf /opt/gdelt-diff/core/gdelt-diff.py /usr/bin/gdelt-diff
sudo ln -sf /opt/gdelt-diff/core/gdelt-live.py /usr/bin/gdelt-live

# Add Service Unit Files
sudo mkdir -p /usr/lib/systemd/system
sudo cp /opt/gdelt-diff/build/gdelt-diff.service /usr/lib/systemd/system/gdelt-diff.service
sudo cp /opt/gdelt-diff/build/gdelt-diff.timer /usr/lib/systemd/system/gdelt-diff.timer
sudo cp /opt/gdelt-diff/build/gdelt-live.service /usr/lib/systemd/system/gdelt-live.service
sudo cp /opt/gdelt-diff/build/gdelt-live.timer /usr/lib/systemd/system/gdelt-live.timer

# Enable Service Unit
sudo systemctl daemon-reload

echo ''
echo Finished Installing GDELT-Diff!
echo ''
echo Make Sure to Edit Your User Config File: /etc/gdelt-diff/config
echo Enable Automatic Downloads With: 'sudo systemctl enable gdelt-diff.timer'
echo Enable Automatic Live Downloads With: 'sudo systemctl enable gdelt-live.timer'
echo ''
