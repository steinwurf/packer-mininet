import os
import glob
import sys
import pathlib

from waflib.Build import BuildContext

VERSION = '1.0.0'


def configure(conf):

    # We need both virtualbox and vagrant installed
    conf.find_program('vagrant')
    conf.find_program('VBoxManage')

    # Ensure that the packer program is available. This is used to build
    # the virtual machine image.
    conf.find_program('packer', exts='',
                      path_list=[str(conf.dependency_path('packer'))])

    conf.find_program('packer-post-processor-vagrant-cloud-standalone', exts='',
                      path_list=[str(conf.dependency_path('packer-vagrant-cloud'))])


def build(bld):

    # Run packer build
    bld.exec_command(f"{bld.env.PACKER[0]} build -except vagrant-cloud -force build.json",
                     stdout=None, stderr=None)


class UploadContext(BuildContext):
    cmd = 'upload'
    fun = 'upload'


def upload(ctx):

    with ctx.create_virtualenv() as venv:

        # To update the requirements.txt just delete it - a fresh one
        # will be generated from test/requirements.in
        if not os.path.isfile('requirements.txt'):
            venv.run('python -m pip install pip-tools')
            venv.run('pip-compile requirements.in')

        venv.run('python -m pip install -r requirements.txt')
        venv.activate()

        import pypandoc
        pypandoc.download_pandoc()
        long_description = pypandoc.convert('NEWS.rst', 'md')

    token_file = os.path.expanduser('~/.vagrantcloud')
    if not os.path.isfile(token_file):
        ctx.fatal("missing .vagrantcloud see README.rst for more information.")

    ctx.exec_command(f"{ctx.env.PACKER[0]} build -var-file {token_file} -var 'version={VERSION}' -var 'version_description={long_description}' upload.json",
                     stdout=None, stderr=None, env={'PACKER_PLUGIN_PATH': ctx.dependency_path('packer-vagrant-cloud')})
