#! /usr/bin/env python
# encoding: utf-8

import os
import sys

import waflib

top = '.'


def resolve(ctx):
    pass

def options(opt):
    pass


def configure(conf):

    # Ensure that the packer program is available. This is used to build
    # the virtual machine image.
    conf.find_program('packer', exts='',
                  path_list=[str(conf.dependency_path('packer'))])

def build(bld):

    # Find the mn.json
    mn = bld.find_file('mn.json', path_list=[bld.path.abspath()])

    print(bld.dependency_path('mininet-vm'))

    ovf = bld.find_file('mininet-2.2.2-170321-ubuntu-14.04.4-server-amd64.ovf',
        path_list=[os.path.join(bld.dependency_path('mininet-vm'),'mn-trusty64server-170321-14-17-08/') ])

    bld.cmd_and_log("%s build -var 'ovf=%s' %s" % (
        bld.env.PACKER[0], ovf, mn), cwd=bld.path)
