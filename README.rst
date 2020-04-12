About
=====

This repository contains a Packer (packer.io) configuration for building
a mininet Vagrant box.

Create and uploading a new box is defined using the following two files:

1. `build.json` this is a Packer JSON file which defines steps building the box.
2. `upload.json` this Packer JSON files defines how we upload the box to
   Vagrant cloud.

The provisioning of the box (i.e. what we install) is defined in `setup.sh`.

Building
--------

To build the box run::

    ./waf configure
    ./waf build

The resulting Vagrant `box` will be in the `build/box` directory.

Upload
------

Once we are happy with the box we can upload it to Vagrant cloud to make it
available to others. To do this you need to get a token for Vagrant Cloud,
you can do this here: https://app.vagrantup.com/settings/security

Once you have a token put it in `.vagrantcloud` in your HOME directory::

    {
        "cloud_token": "your_token_here"
    }

After this you can run::

    ./waf upload


