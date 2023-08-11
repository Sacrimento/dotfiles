#!/usr/bin/bash

killall xss-lock
killall conky

slack &
dunst &
nm-applet &
drata-agent &
picom --experimental-backend -b &
xss-lock -- betterlockscreen -q -l blur -- --bar-indicator --bar-orientation=vertical --bar-color=00000000 --bar-pos=365:h-129 --bar-base-width=10 --bar-total-width=100 &
conky -c ~/.config/conky/dracula.conkyrc &
