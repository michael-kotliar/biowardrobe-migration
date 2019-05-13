#! /usr/bin/env python3

import pkg_resources
from os import symlink, path
from time import strftime, gmtime
from setuptools import setup, find_packages
from setuptools.command.egg_info import egg_info
from subprocess import check_output, CalledProcessError


SETUPTOOLS_VER = pkg_resources.get_distribution("setuptools").version.split('.')
RECENT_SETUPTOOLS = int(SETUPTOOLS_VER[0]) > 40 or \
                    (int(SETUPTOOLS_VER[0]) == 40 and int(SETUPTOOLS_VER[1]) > 0) or \
                    (int(SETUPTOOLS_VER[0]) == 40 and int(SETUPTOOLS_VER[1]) == 0 and int(SETUPTOOLS_VER[2]) > 0)


class EggInfoFromGit(egg_info):

    def git_timestamp_tag(self):
        gitinfo = check_output(['git', 'log', '--first-parent', '--max-count=1', '--format=format:%ct', '.']).strip()
        return strftime('.%Y%m%d%H%M%S', gmtime(int(gitinfo)))

    def tags(self):
        if self.tag_build is None:
            try:
                self.tag_build = self.git_timestamp_tag()
            except CalledProcessError:
                pass
        return egg_info.tags(self)

    if RECENT_SETUPTOOLS:
        vtags = property(tags)


tagger = EggInfoFromGit


setup(
    name='biowardrobe-migration',
    version="1.0",
    license = 'Apache-2.0',
    description="BioWardrobe-to-Biowardrobe-NG migration package",
    author='Michael Kotliar',
    author_email='misha.kotliar@gmail.com',

    long_description=open(path.join(path.dirname(__file__), 'README.md')).read(),
    long_description_content_type="text/markdown",

    url="https://github.com/michael-kotliar/biowardrobe-migration",
    download_url="https://github.com/michael-kotliar/biowardrobe-migration",
    
    cmdclass={'egg_info': tagger},
    packages=find_packages(),
    install_requires=[],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            "biowardrobe-migration=biowardrobe_migration.main:main"
        ]
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: OS Independent',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: Microsoft :: Windows :: Windows 8.1',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ]
)
