.. _releases:

********
Releases
********

.. release:: 0.1.2
    :date: 2016-12-01

    .. change:: fixed
        :tags: extensions

        Able to tell cerda to collect specific file types.
        ``--customType bmp,fbx,abc``
        `Read more <https://github.com/docwhite/cerda/issues/7>`_

    .. change:: new
        :tags: thumbnails

        Thumbnail support. When sending an email if the file that has been
        collected is an image type cerda generates a .png preview and attaches
        it into the email that sends.
        `Read more <https://github.com/docwhite/cerda/issues/6>`_

    .. change:: changed
        :tags: listener

        On Houdini for cerda to know about a frame being completed it checks if
        the .mantra_checkpoint still exists. If it does it means rendering is
        not finished. `Read more <https://github.com/docwhite/cerda/issues/4>`_

    .. change:: changed
        :tags: improvement

        Regular expressions run on the paths the user inputs to check that it
        is legal. `Read more <https://github.com/docwhite/cerda/issues/1>`_


.. release:: 0.1.1
    :date: 2016-06-06

    .. change:: fixed
        :tags: extensions

        Fixed Dropbox path issues.

    .. change:: changed
        :tags: commands

        Refactored bad commands in documentation.

.. release:: 0.1.0
    :date: 2016-10-06

    .. change:: new
        :tags: local, transfer

        Local transferring.

    .. change:: new
        :tags: dropbox, transfer

        Dropbox transferring.

    .. change:: new
        :tags: interface

        Email notification. User can receive an email after ``--count N`` frames
        get dropped.

    .. change:: new
        :tags: local, transfer

        Logging to file (debug level) and standard output (info level)

        