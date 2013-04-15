Jmbo Downloads User Guide
=========================

Jmbo Downloads allows you to easily create and serve downloadable content on your Jmbo sites. Files are uploaded via the admin interface, or generated per request,
and served by your webserver. These downloads can then be tracked - Jmbo Downloads, by default, tracks the total downloads for each item.

To add or modify downloadable content, navigate to Downloads in the admin interface. A basic download lets you specify the file to be downloaded and, optionally, a file name to serve the file with.
Users can view all downloads by navigating to www.yoursite.com/downloads.

Installation
------------

1. Add ``downloads`` to INSTALLED_APPS.
2. Run ``manage.py migrate downloads`` (requires South).
3. If you are using Nginx:
    - Define an internal location at MEDIA_URL/downloads/(.*) in your site's Nginx config.
    - Set its alias to MEDIA_ROOT/downloads/$1.
    - If you are using Jmbo with buildout, add this to the appropriate buildout template.
4. If you are using another webserver you will have to specify the internal redirection header by putting ``DOWNLOAD_INTERNAL_REDIRECT_HEADER`` in your settings.
5. If files are hosted remotely set ``DOWNLOAD_SERVE_FROM`` to 'REMOTE'. The client will be redirected to the remote location.

Requirements
------------

- Django 1.3 and above
- Jmbo and all its requirements
- South

Other features (the fun stuff)
------------------------------

Generated files
***************

You might want to serve a file that is generated on the fly, for example a PDF with the user's details in it. You can do this by subclassing ``models.TemporaryDownloadAbstract``.
The child class must implement the function ``def create_file(self, file_path, request)``. Generate your file in this function and save it at ``file_path`` (it includes the file name).
You can use the ``request`` object to access the ``user`` object and query string parameters.

You can optionally specify a file name and extension by overriding ``def make_file_name(self, request)``. Call the superclass function and provide the ``extension`` argument
to get a UUID + extension as the file name. Otherwise return your own unique file name. Keep in mind that the file will only be served with its on-disk name if the model's file name field is empty.
If the field has been specified, all generated files are served with the specified file name.

Only one implementation of ``models.TemporaryDownloadAbstract`` is included with Jmbo Downloads: ``models.TextOverlayTemporaryDownload``. This download takes a background image, draws some text on it and saves it as a JPEG.

Note that all generated files are generated upon request and stored in MEDIA_ROOT/downloads/tmp/. You need to clear out this folder periodically to avoid running out of disk space.

Tracking downloads
******************

If you would like to track more than just the number of downloads (or view count) per item you can implement a receiver for ``signals.download_requested``. The signal will pass a download instance (as ``sender``) and the ``request`` object to the receiver.
This allows for stats like downloads by time of day and a user's favourite download categories to be tracked.
