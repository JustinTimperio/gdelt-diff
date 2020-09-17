#!/usr/bin/env bash

sudo rm -Rf /opt/gdelt-diff
sudo rm -Rf /etc/gdelt-diff
sudo rm /usr/bin/gdelt-diff
sudo rm /usr/bin/gdelt-live
sudo rm /usr/lib/systemd/system/gdelt-diff.service
sudo rm /usr/lib/systemd/system/gdelt-diff.timer
sudo rm /usr/lib/systemd/system/gdelt-live.service
sudo rm /usr/lib/systemd/system/gdelt-live.timer
sudo rm -Rf /tmp/gdelt-live 

# Enable Service Unit
sudo systemctl daemon-reload

echo Finished Removing GDELT-Diff!
