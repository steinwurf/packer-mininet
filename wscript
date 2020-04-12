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

    upload_json = ctx.path.find_node('upload.json')

    if not upload_json:
        ctx.fatal("Could not find upload.json")

    box = ctx.path.find_node('build/box/package.box')

    if not box:
        ctx.fatal("Could not find box")

    # To use the vagrant-cloud-standalone plugin we need to do two things:
    # 1) Use version 1.4.5 of packer (since version 1.5.x is not yet compatible
    #    with the plugin). See issue:
    #    https://github.com/armab/packer-post-processor-vagrant-cloud-standalone/issues/6
    #
    # 2) Run the packer command with a cwd of the vagrant-cloud-plugin since
    #    version 1.4.5 of packer does not support the PACKER_PLUGIN_PATH
    #    environment variable.
    #
    # So once vagrant-cloud-standalone supports version 1.5.x of packer we
    # can avoid this.
    ctx.exec_command((f"{ctx.env.PACKER[0]} build "
                      f"-var-file {token_file} "
                      f"-var 'version={VERSION}' "
                      f"-var 'box={box}' "
                      f"-var 'version_description={long_description}' "
                      f"{upload_json}"),
                     stdout=None, stderr=None,
                     cwd=ctx.dependency_path('packer-vagrant-cloud'))
