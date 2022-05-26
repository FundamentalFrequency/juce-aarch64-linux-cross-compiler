#!/bin/bash
export TEXTDOMAIN=arandr

. gettext.sh

zenity --password --title "$(gettext "Password Required")"

