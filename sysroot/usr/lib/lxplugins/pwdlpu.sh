#!/bin/bash
export TEXTDOMAIN=lxplug-updater

. gettext.sh

zenity --password --title "$(gettext "Password Required")"

