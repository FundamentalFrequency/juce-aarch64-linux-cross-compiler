#!/bin/bash
export TEXTDOMAIN=gui-pkinst

. gettext.sh

zenity --password --title "$(gettext "Password Required")"

