
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

setup(
    name='cerda',
    version='0.1.1',
    description='An NCCA renderfarm SFTP watcher',
    url='https://github.com/docwhite/cerda',
    download_url='https://github.com/docwhite/cerda/tarball/0.1.1',
    author='Ramon Blanquer',
    author_email='blanquer.ramon@gmail.com',
    license='MIT',
    keywords='renderfarm ncca transfer files watch notification email dropbox',
    packages=find_packages(exclude=['docs', 'test']),
    install_requires=['coloredlogs', 'dropbox', 'pysftp'],
    extras_require={
        'docs': ['Sphinx', 'sphinx-rtd-theme'],
        'test': ['pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'cerda=cerda:main',
        ],
    },
)