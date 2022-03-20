#!/usr/bin/bash

slack &
nm-applet &
blueman-manager &
volumeicon &
picom --experimental-backend -b &
feh --bg-scale /usr/share/backgrounds/xfce/abstract-1779631.jpg

