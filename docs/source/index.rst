cerda
=====

.. note ::
    This is intended to be used at NCCA labs only.

Installation
------------

If you are in the labs you will need to install pip locally. Follow these
steps carefully:

Open a terminal and change directory to home::
    
    $ cd ~

Get the pip installer script with wget (downloads a file form the web)::
    
    $ wget https://bootstrap.pypa.io/get-pip.py -P ~

Install pip locally (it will get installed to ``~/.local``)::
    
    $ python ~/.get-pip --user

Append the binaries directory that contains all the pip executables to your
``$PATH`` variable. Either do it manually or simply execute this line of code
that will write a new line on your ``.bashrc`` file::
    
    $ echo "PATH=\$PATH:~/.local/bin" >> ~/.bashrc


Close the shell and start a new one. Alternatively reload your profile::

    $ source ~/.bashrc

Now you got all the dependencies installed! The next move is to download the
release of watcharm and install it!

Usage
-----

::

    cerda -h
    usage: cerda [-h] [-s SOURCE] [-d DESTINATION]

    Process credentials and paths for farm watcher

    optional arguments:
        -h, --help
            Show this help message and exit
        -s SOURCE, --source SOURCE
            Remote location path (relative to home) where the
            frames get generated.
        -d DESTINATION, --destination DESTINATION
            Destination location path where you would like the
            frames to get sent to.

.. warning ::
    Please make sure the **paths** you pass in are relative to your home folder

Examples
--------

My renderfarm is rendering out the frames at ``/home/i7243466/project1/render`` 
on the **tete** server. I want the frames to get transfered to my local drive at
location ``/home/i7243466/rendered/frames``::

    $ cerda --source project1/render --destination rendered/frames

Or you could also use the short flags::

    $ cerda -s project1/render --destination rendered/frames



.. automodule:: farm_watcher
   :members:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

