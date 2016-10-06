cerda
#####

.. image:: https://docwhite.github.io/cerda/_images/cerda_with_help.png

Welcome to Cerda's documentation. This tool will allow you to transfer the files
that get rendered at renderfarm to either local disk or Dropbox account. Also 
there is a notification feature that allows you to get sent an email after a 
specific number of frames get rendered. Cool, innit?

* *Documentation:* https://docwhite.github.io/cerda
* *Source:* https://github.com/docwhite/cerda
* *Bugs:* https://github.com/docwhite/cerda/issues

**NOTE:** This is intended to be used at NCCA labs only.

Follow these steps in the labs. I wrote how to install pip locally because we
don't have sudo privileges, pity. No worries it is literally **3 lines of code**
as I like to keep things simple.

**WARNING:** This tool is in early stage. Please contribute reporting issues on
http://github.com/docwhite/cerda or directly by speaking to that Spanish shy
guy in the labs, or drop me an email blanquer.ramon@gmail.com

Upcoming features:

* **Direct integration with Qube**: There will be no need to do all the steps to
  dispatch the job to the render farm.
* Improved mail formatting with **thumbnails** of what has been rendered.

Prerequisites
=============

If you are in the labs you will need to install pip locally. Follow these
steps carefully:

Open a terminal and change directory to home::
    
    $ cd ~

Get the pip installer script with wget (downloads a file form the web)::
    
    $ wget https://bootstrap.pypa.io/get-pip.py -P ~

Install pip locally (it will get installed to ``~/.local``)::
    
    $ python ~/get-pip.py --user
    
Append the binaries directory that contains all the pip executables to your
``$PATH`` variable. Either do it manually or simply execute this line of code
that will write a new line on your ``.bashrc`` file::
    
    $ echo "PATH=\$PATH:~/.local/bin" >> ~/.bashrc

Close the shell and start a new one. Alternatively reload your profile::

    $ source ~/.bashrc

Installation
============

Now you got pip up and running! The next move is to install the tool using it::

    $ pip install cerda --user
    
Usage
=====

Check out the help command ``cerda -h``::

    usage: cerda [-h] [-dbox] [-e EMAIL] [-c COUNT] [-r EVERY] source target

    An NCCA render farm collector.

    positional arguments:
      source                Remote location path (relative to home) where the
                            frames get generated.
      target                Destination location path where you would like the
                            frames to get sent to.

    optional arguments:
      -h, --help            show this help message and exit
      -dbox, --dropbox      Will send the files to the root path of your dropbox
                            account.
      -e EMAIL, --email EMAIL
                            Email address to send notification to after -c frames
                            have been rendered.
      -c COUNT, --count COUNT
                            At this numer of frames, send an email to the address
                            specified with -m flag.
      -r EVERY, --every EVERY
                            How often to check for frames dropped (in seconds)

**WARNING:** Please make sure the **paths** you pass in are relative to your home folder.

Examples
++++++++

Example 1
---------

My renderfarm is rendering out the frames at ``/home/i7243466/project1/render`` 
on the **tete** server. I want the frames to get transfered to my local drive at
location ``/home/i7243466/rendered/frames``::

    $ cerda project1/render rendered/frames

Or you could also use the short flags::

    $ cerda project1/render rendered/frames

Example 2
---------

My renderfarm is rendering out the frames at ``/home/i7243466/project1/render`` 
on the **tete** server. I want the frames to get transfered to my Dropbox
account under ``/some/folder``::

    $ cerda project1/render some/folder --dropbox

Or::

    $ cerda project1/render rendered/frames -dbox

Example 3
---------

My renderfarm is rendering out the frames at ``/home/i7243466/project1/render`` 
on the **tete** server. I want the frames to get transfered to my Dropbox
account under ``/some/folder`` **and** when it has finished rendering, which
means 20 frames get collected, send me an email notification::

    $ cerda project1/render some/folder --dropbox --email blanquer.ramon@gmail.com --count 20

Or::

    $ cerda project1/render rendered/frames -dbox -e blanquer.ramon@gmail.com -c 20

When it is finished you will receive an email from **cerdancca@gmail.com**.
Hopefully it won't get blocked as I am using Google's own SMTP servers.

If you find any problem or bug please report it using the Issues page or drop me a line at blanquer.ramon@gmail.com
