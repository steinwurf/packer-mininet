About
=====

This repository contains a Packer (packer.io) configuration for building
a mininet Vagrant box.

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


