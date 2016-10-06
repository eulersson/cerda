.. _usage:

*****
Usage
*****

::

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

.. warning::
    Please make sure the **paths** you pass in are relative to your home folder

Examples
========

Example 1
---------

My renderfarm is rendering out the frames at ``/home/i7243466/project1/render`` 
on the **tete** server. I want the frames to get transfered to my local drive at
location ``/home/i7243466/rendered/frames``::

    $ cerda --source project1/render --target rendered/frames

Or you could also use the short flags::

    $ cerda -s project1/render --t rendered/frames

Example 2
---------

My renderfarm is rendering out the frames at ``/home/i7243466/project1/render`` 
on the **tete** server. I want the frames to get transfered to my Dropbox
account under ``/some/folder``::

    $ cerda --source project1/render --target some/folder --dropbox

Or::

    $ cerda -s project1/render -t rendered/frames -dbox

Example 3
---------

My renderfarm is rendering out the frames at ``/home/i7243466/project1/render`` 
on the **tete** server. I want the frames to get transfered to my Dropbox
account under ``/some/folder`` **and** when it has finished rendering, which
means 20 frames get collected, send me an email notification::

    $ cerda --source project1/render --target some/folder --dropbox --email blanquer.ramon@gmail.com --count 20

Or::

    $ cerda -s project1/render -t rendered/frames -dbox -e blanquer.ramon@gmail.com -c 20

When it is finished you will receive an email from **cerdancca@gmail.com**.
Hopefully it won't get blocked as I am using Google's own SMTP servers.