#!/usr/bin/env bash

# Exit immediately if command fails:
#     https://stackoverflow.com/a/19622569/1717320
set -e

# Print a trace of all commands
set -x

# Updating and Upgrading dependencies
#sudo apt-get update -y -qq > /dev/null
#sudo apt-get upgrade -y -qq > /dev/null

# Install necessary libraries for guest additions and Vagrant NFS Share
apt-get -y -q install linux-headers-$(uname -r) build-essential dkms nfs-common

# Install wget to get public key from upstream.
# May already be installed, but we make sure.
apt-get install -y --force-yes wget

# Set up sudo
useradd --create-home vagrant
echo 'vagrant ALL=NOPASSWD:ALL' > /etc/sudoers.d/vagrant

# Install vagrant key
mkdir -pm 700 /home/vagrant/.ssh
wget --no-check-certificate https://raw.github.com/mitchellh/vagrant/master/keys/vagrant.pub -O /home/vagrant/.ssh/authorized_keys
chmod 0600 /home/vagrant/.ssh/authorized_keys
chown -R vagrant:vagrant /home/vagrant

# Customize the message of the day
echo 'Development Environment' > /etc/motd

# Install the VirtualBox guest additions
VBOX_VERSION=$(cat .vbox_version)
VBOX_ISO=VBoxGuestAdditions_$VBOX_VERSION.iso
mount -o loop $VBOX_ISO /mnt
/mnt/VBoxLinuxAdditions.run
umount /mnt

#Cleanup VirtualBox
rm $VBOX_ISO
