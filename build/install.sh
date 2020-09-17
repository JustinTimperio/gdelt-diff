#!/usr/bin/env bash

# Clone Repo
git clone https://github.com/JustinTimperio/gdelt-diff.git /opt/gdelt-diff

# Add Config to /etc
mkdir -p /etc/gdelt-diff
cp /opt/gdelt-diff/build/config /etc/gdelt-diff/config
ln -sf /opt/gdelt-diff/core/gdelt-diff.py /usr/bin/gdelt-diff
ln -sf /opt/gdelt-diff/core/gdelt-live.py /usr/bin/gdelt-live

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
