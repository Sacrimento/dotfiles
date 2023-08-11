#!/usr/bin/env bash

set -euo pipefail

function ensure() {
    if [ $(printf 'No\nYes' | rofi -dmenu -p "Are you sure") == "No" ]; then
        exit 0
    fi
}

options=("Lock" "Logout" "Shutdown")

choice=$(printf '%s\n' "${options[@]}" | rofi -dmenu -p Action)

case "$choice" in
"Lock")
    loginctl lock-session
    ;;
"Logout")
    ensure
    qtile cmd-obj -o cmd -f shutdown
    ;;
"Shutdown")
    ensure
    systemctl poweroff
    ;;
*)
    exit 0
    ;;
esac
