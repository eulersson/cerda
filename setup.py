from setuptools import setup, find_packages

requires = [
    'coloredlogs',
    'dropbox',
    'pysftp',
    'imageio',
    'cffi',
    'numpy',
    'python-resize-image'
]

test_requires = [
    'coverage',
    'pytest',
    'pytest-cov',
    'enum'
]

doc_requires = [
    'Sphinx',
    'sphinx-rtd-theme'
]

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
    install_requires=requires,
    test_requires=test_requires,
    extras_require={
        'docs': doc_requires,
        'test': test_requires,
    },
    entry_points={
        'console_scripts': [
            'cerda=cerda:main',
        ],
    },
)
