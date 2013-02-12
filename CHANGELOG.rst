Changelog
=========

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
