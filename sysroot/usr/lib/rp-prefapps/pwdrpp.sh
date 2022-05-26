#!/bin/bash
export TEXTDOMAIN=rp-prefapps

. gettext.sh

zenity --password --title "$(gettext "Password Required")"

