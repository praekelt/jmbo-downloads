Changelog
=========

2.0.0
-----
#. Stabilize on jmbo 2.0.0.

2.0.0a1
-------
#. Get tests to pass again.
#. Django 1.6 support.
#. Up minimum jmbo to 2.0.0.

0.0.8
-----
#. Correct calculation of download URL, particularly for temporary downloads.
#. Lots of PEP8 fixes.

0.0.7
-----
#. Temporary downloads adhere to `DOWNLOAD_SERVE_FROM` setting. They are always created on the local filesystem though. If 'REMOTE' is used the developer needs to sync these files with a remote filesystem.

0.0.6
-----
#. Add `DOWNLOAD_INTERNAL_REDIRECT_HEADER` setting (default 'X-Accel-Redirect') in case a webserver other than Nginx is used.
#. Add `DOWNLOAD_SERVE_FROM` setting (default 'LOCAL') to specify whether to serve the files locally or redirect to a remote location.

0.0.5
-----
#. Fix bug where X-Accel-Redirect uses file name override instead of actual file name to serve download, causing a 404 if the file name and override don't match.

0.0.4 (2012-06-21)
------------------
#. South dependency on jmbo upped to 0002 migration.

0.0.3 (2012-06-15)
------------------
#. Improve templates to better render download categories.
#. Override Jmbo's PermittedManager to exclude invisible downloads from querysets.
#. Make ImageMod more generic and rename it to TemporaryDownloadAbstract.
#. Send signal when a download is requested, allowing other apps to track downloads.
#. Miscellaneous small fixes.

0.0.2
------------------
#. Add everything to manifest for PyPI release.

0.0.1 (2012-05-28)
------------------
#. Initial release.
