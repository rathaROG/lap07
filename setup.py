#!/usr/bin/env python

# # # # # # # # # # # # # # # # # # # # # # # # #
# Updated 2023/06/20: Make simplier by rathaROG #
# # # # # # # # # # # # # # # # # # # # # # # # #

import os
import shutil
import subprocess
import sys

DISTNAME = 'lap07'
DESCRIPTION = "Customized edition of lap - Linear Assignment Problem solver (LAPJV/LAPMOD)."
LONG_DESCRIPTION = """
**lap** is a linear assignment problem solver using Jonker-Volgenant
algorithm for dense (LAPJV) or sparse (LAPMOD) matrices.
"""
MAINTAINER = 'rathaROG'
URL = 'https://github.com/rathaROG/lap07'
LICENSE = 'BSD (2-clause)'
DOWNLOAD_URL = URL

NUMPY_MIN_VERSION = '1.10.1'

SETUPTOOLS_COMMANDS = set([
    'develop', 'release', 'bdist_egg', 'bdist_rpm',
    'bdist_wininst', 'install_egg_info', 'build_sphinx',
    'egg_info', 'easy_install', 'upload', 'bdist_wheel',
    '--single-version-externally-managed',
])

if SETUPTOOLS_COMMANDS.intersection(sys.argv):
    extra_setuptools_args = dict(
        zip_safe=False,  # the package can run out of an .egg file
        include_package_data=True,
        extras_require={
            'alldeps': (
                'numpy >= {0}'.format(NUMPY_MIN_VERSION),
            ),
        },
    )
else:
    extra_setuptools_args = dict()

from distutils.command.clean import clean as Clean
class CleanCommand(Clean):
    description = "Remove build artifacts from the source tree"
    def run(self):
        Clean.run(self)
        if os.path.exists('build'):
            shutil.rmtree('build')
        # Remove c files if we are not within a sdist package
        cwd = os.path.abspath(os.path.dirname(__file__))
        remove_c_files = not os.path.exists(os.path.join(cwd, 'PKG-INFO'))
        if remove_c_files:
            if os.path.exists('lap/_lapjv.cpp'):
                os.unlink('lap/_lapjv.cpp')
        for dirpath, dirnames, filenames in os.walk('lap'):
            for filename in filenames:
                if any(filename.endswith(suffix) for suffix in
                       (".so", ".pyd", ".dll", ".pyc")):
                    os.unlink(os.path.join(dirpath, filename))
            for dirname in dirnames:
                if dirname == '__pycache__':
                    shutil.rmtree(os.path.join(dirpath, dirname))

cmdclass = {'clean': CleanCommand}

def cythonize(cython_file, gen_file):
    flags = ['--fast-fail']
    if gen_file.endswith('.cpp'): flags += ['--cplus']
    try:
        try:
            rc = subprocess.call(['cython'] + flags + ["-o", gen_file, cython_file])
            if rc != 0: raise Exception('Cythonizing %s failed' % cython_file)
        except OSError:
            # There are ways of installing Cython that don't result in a cython
            # executable on the path, see scipy issue gh-2397.
            rc = subprocess.call([sys.executable, '-c',
                                  'import sys; from Cython.Compiler.Main '
                                  'import setuptools_main as main;'
                                  ' sys.exit(main())'] + flags +
                                 ["-o", gen_file, cython_file])
            if rc != 0: raise Exception('Cythonizing %s failed' % cython_file)
    except OSError:
        raise OSError('Cython needs to be installed')

def get_wrapper_pyx():
    return os.path.join('lap', '_lapjv.pyx')

def generate_cython():
    wrapper_pyx_file = get_wrapper_pyx()
    wrapper_c_file = os.path.splitext(wrapper_pyx_file)[0] + '.cpp'
    cythonize(wrapper_pyx_file, wrapper_c_file)

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_numpy_include_dirs
    config = Configuration(None, parent_package, top_path)
    config.set_options(ignore_setup_xxx_py=True, 
                       assume_default_configuration=True, 
                       delegate_options_to_subpackages=True, 
                       quiet=True)
    config.add_data_dir('lap/tests')

    wrapper_pyx_file = get_wrapper_pyx()
    wrapper_c_file = os.path.splitext(wrapper_pyx_file)[0] + '.cpp'
    c_files = [
            os.path.join(os.path.dirname(wrapper_pyx_file), 'lapjv.cpp'),
            os.path.join(os.path.dirname(wrapper_pyx_file), 'lapmod.cpp')]
    config.add_extension('lap._lapjv', sources=[wrapper_c_file, c_files],
                         include_dirs=[get_numpy_include_dirs(), 'lap'])

    return config

def get_version_string():
    version_py = "lap/__init__.py"
    with open(version_py) as version_file:
        for line in version_file.read().splitlines():
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]

def setup_package():
    metadata = dict(name=DISTNAME,
                    maintainer=MAINTAINER,
                    description=DESCRIPTION,
                    license=LICENSE,
                    packages=['lap'],
                    url=URL,
                    version=get_version_string(),
                    download_url=DOWNLOAD_URL,
                    long_description=LONG_DESCRIPTION,
                    classifiers=['Development Status :: 4 - Beta',
                                 'Environment :: Console',
                                 'Intended Audience :: Science/Research',
                                 'Intended Audience :: Developers',
                                 'Programming Language :: C',
                                 'Programming Language :: Python',
                                 'Programming Language :: Python :: 2',
                                 'Programming Language :: Python :: 3',
                                 'Programming Language :: Python :: 2.7',
                                 'Programming Language :: Python :: 3.7',
                                 'Programming Language :: Python :: 3.8',
                                 'Programming Language :: Python :: 3.9',
                                 'Operating System :: Microsoft :: Windows',
                                 'Operating System :: POSIX',
                                 'Operating System :: Unix',
                                 'Operating System :: MacOS',
                                ],
                    cmdclass=cmdclass,
                    **extra_setuptools_args)

    if len(sys.argv) == 1 or (
            len(sys.argv) >= 2 and ('--help' in sys.argv[1:] or
                                    sys.argv[1] in ('--help-commands',
                                                    'egg_info',
                                                    '--version',
                                                    'clean'))):
        try:
            from setuptools import setup
        except ImportError:
            from distutils.core import setup
    else:
        from numpy.distutils.core import setup
        metadata['configuration'] = configuration
        if len(sys.argv) >= 2 and sys.argv[1] not in 'config':
            print('Generating cython files')
            generate_cython()
    setup(**metadata)

def install_reqs():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Cython"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])

if __name__ == "__main__":
    install_reqs()
    setup_package()
