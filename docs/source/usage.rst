.. _usage:

*****
Usage
*****

::

    usage: cerda [-h] [-dbox] [-e EMAIL] [-c COUNT] [-r EVERY] [-t CUSTOMTYPES]
                 source target

    An NCCA render farm collector.

    positional arguments:
      source                Remote location path (relative to home) where the
                            frames get generated.
      target                Custom file extensions to mark for transfering. I.e.
                            -t tiff,exr,obj

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
      -t CUSTOMTYPES, --customTypes CUSTOMTYPES
                            Custom file extensions to mark for transfering. I.e.
                            -t tiff,exr,obj

.. warning::
    Please make sure the **paths** you pass in are relative to your home folder

Examples
========

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

Example 4
---------

My renderfarm is rendering out Alembic **.abc** files at ``/home/i7243466/project1/render`` 
on the **tete** server. I want the files to get transfered to my local drive at
location ``/home/i7243466/hello/alembics``::

    $ cerda project1/render hello/alembics --customTypes abc

Or you could also use the short flags::

    $ cerda project1/render hello/alembics --t abc

.. note::
    You can specify more than custom type to transfer like ``--customTypes png,jpg,abc,tiff``
    No spaces, separated by commas.