#!/usr/bin/env bash

# Remove Core Files
sudo rm -Rf /opt/gdelt-diff
sudo rm -Rf /etc/gdelt-diff
sudo rm /usr/bin/gdelt-diff
sudo rm /usr/bin/gdelt-live
sudo rm -Rf /tmp/gdelt-live 

# Disable Service Units
sudo systemctl stop gdelt-diff.timer gdelt-live.timer
sudo systemctl disable gdelt-diff.timer gdelt-live.timer
sudo rm /usr/lib/systemd/system/gdelt-diff.service
sudo rm /usr/lib/systemd/system/gdelt-diff.timer
sudo rm /usr/lib/systemd/system/gdelt-live.service
sudo rm /usr/lib/systemd/system/gdelt-live.timer
sudo systemctl daemon-reload

echo ''
echo Finished Removing GDELT-Diff!
echo ''
