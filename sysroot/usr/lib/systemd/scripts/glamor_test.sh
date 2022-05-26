#!/bin/bash

# Glamor should run unless the platform is not Pi 4 and the legacy driver is not in use.

if ! raspi-config nonint is_pifour && raspi-config nonint is_kms ; then
	if ! [ -e /usr/share/X11/xorg.conf.d/20-noglamor.conf ] ; then
		cat > /usr/share/X11/xorg.conf.d/20-noglamor.conf << EOF
Section "Device"
	Identifier "kms"
	Driver "modesetting"
	Option "AccelMethod" "none"
EndSection
EOF
	fi
else
	if [ -e /usr/share/X11/xorg.conf.d/20-noglamor.conf ] ; then
		rm /usr/share/X11/xorg.conf.d/20-noglamor.conf
	fi
fi
