.. _prerequisites:

*************
Prerequisites
*************

If you are in the labs you will need to install pip locally. Follow these
steps carefully:

Open a terminal and change directory to home::
    
    $ cd ~

Get the pip installer script with wget (downloads a file form the web)::
    
    $ wget https://bootstrap.pypa.io/get-pip.py -P ~

.. note::
    If you are wondering what is pip, think of it as a package manager for
    Python modules. Like apt-get or yum but just for tools written in Python.

Install pip locally (it will get installed to ``~/.local``)::
    
    $ python ~/.get-pip --user

Append the binaries directory that contains all the pip executables to your
``$PATH`` variable. Either do it manually or simply execute this line of code
that will write a new line on your ``.bashrc`` file::
    
    $ echo "PATH=\$PATH:~/.local/bin" >> ~/.bashrc

Close the shell and start a new one. Alternatively reload your profile::

    $ source ~/.bashrc

Done!