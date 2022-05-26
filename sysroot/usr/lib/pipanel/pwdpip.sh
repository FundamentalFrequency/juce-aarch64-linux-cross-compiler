#!/bin/bash
export TEXTDOMAIN=pipanel

. gettext.sh

zenity --password --title "$(gettext "Password Required")"

