
from setuptools import setup, find_packages

setup(
    name='watchfarm',
    version='0.1.0',
    description='An NCCA renderfarm SFTP watcher',
    url='https://github.com/docwhite/watchfarm',
    author='Ramon Blanquer',
    author_email='blanquer.ramon@gmail.com',
    license='MIT',
    keywords='renderfarm ncca transfer files watch',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=['coloredlogs', 'dropbox', 'pysftp'],
    extras_require={
        'docs': ['Sphinx', 'sphinx_rtd_theme'],
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'watchfarm=watchfarm:main',
        ],
    },
)