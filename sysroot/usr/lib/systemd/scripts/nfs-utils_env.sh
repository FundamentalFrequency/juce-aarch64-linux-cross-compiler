#!/bin/sh
# Create /run/sysconfig/nfs-utils from NFS' /etc/default/ files, for
# nfs-config.service

nfs_config=/etc/sysconfig/nfs
[ -r /etc/default/nfs-common ] && . /etc/default/nfs-common
[ -r /etc/default/nfs-kernel-server ] && . /etc/default/nfs-kernel-server

mkdir -p /run/sysconfig
{
echo PIPEFS_MOUNTPOINT=/run/rpc_pipefs
echo RPCNFSDARGS=\"$RPCNFSDOPTS ${RPCNFSDCOUNT:-8}\"
echo RPCMOUNTDARGS=\"$RPCMOUNTDOPTS\"
echo STATDARGS=\"$STATDOPTS\"
# The rpc-svcgssd.service systemd file uses SVCGSSDARGS, not
# RPCSVCGSSDARGS, but for a long time just the latter was exported.
# To not break upgrades for people who have worked around this by
# overriding the systemd service to use RPCSVCGSSDARGS, both variables
# are being exported now.
# See https://bugs.launchpad.net/bugs/1616123 and
# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=892654 for more details.
echo GSSDARGS=\"$RPCGSSDOPTS\"
echo RPCSVCGSSDARGS=\"$RPCSVCGSSDOPTS\"
echo SVCGSSDARGS=\"$RPCSVCGSSDOPTS\"
} > /run/sysconfig/nfs-utils

# the following are supported by the systemd units, but not exposed in default files
# echo SMNOTIFYARGS=\"$SMNOTIFYARGS\"
# echo RPCIDMAPDARGS=\"$RPCIDMAPDARGS\"
# echo BLKMAPDARGS=\"$BLKMAPDARGS\"
# echo GSS_USE_PROXY=\"$GSS_USE_PROXY\"
