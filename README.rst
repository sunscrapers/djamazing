-----------------------------------------------
Djamazing - a safe storage for AWS
-----------------------------------------------

Djamazing [d͡ʒəˈmeɪzɪŋ] offers a way to use S3+Cloudfront as Django Storage. It has the
benefit over conventional storages, that it generates signed URLs, so only the
user who was able to display the URL is also able to access it. Djamazing
can work in two modes:

    unprotected mode
        In this mode the storage simply generates URL-s to cloudfront. The
        cloudfront distribution should be publicly accessible. This can be used
        for files that don't require special security.

    protected mode
        The URLs are signed in this model using the ``SECRET_KEY``. These
        signatures are only valid for the current user. Please remember that
        it is *up to the developer* to ensure that the signed URLs are created
        only when the user that can access them is logged in (some kind of
        per-row authorization should probably be in place).  After clicking
        these a special view redirects the user to a signed cloudfront URL.
        This URL is only valid for one second.

AWS configuration
-------------------------

1. Create an S3 bucket.
2. Generate a keypair for the user that can access the bucket.
3. Create a cloudfront distribution that has origin in the bucket and is
   restricted to signed URLs.
4. (for protected mode) Generate a cloudfront keypair that can be used in
    the distribution.

Installation
------------------------

1. Install djamazing by pip.
2. Set ``"djamazing.storage.DjamazingStorage"`` as your DEFAULT_FILE_STORAGE.
3. Configure Djamazing::
   
    DJAMAZING = {
        'CLOUDFRONT_KEY': b"""-----BEGIN RSA PRIVATE KEY-----                                                 
    (...)
    -----END RSA PRIVATE KEY-----""",
        'CLOUDFRONT_KEY_ID': '...',
        'CLOUDFRONT_URL': 'http://....cloudfront.net/', 
        'S3_KEY_ID': '...',
        'S3_SECRET_KEY': '...',
        'S3_BUCKET': '...',
    }

   For unprotected mode omit the ``CLOUDFRONT_KEY`` and ``CLOUDFRONT_KEY_ID``
   keys.
   The parameter ``CLOUDFRONT_KEY`` may be also given by file path.
4. Add threadlocals middleware
   ``'threadlocals.middleware.ThreadLocalMiddleware'`` to your ``MIDDLEWARE``
5. Add djamazing URLs to ``urls.py``::

    url(r'^djamazing/', include(djamazing.urls)),

Using various configurations in one project
-----------------------------

If you want to use various configurations in one project (e.g. unprotected for
static file and protected for uploads), you can use inheritance. Create a
simple subclass of ``DjamazingStorage`` like::

    class StaticStorage(DjamazingStorage):
        """Storage for static files"""

        def __init__(self):
            super(StaticStorage, self).__init__(settings.STATIC_DJAMAZING)

now you can use it as your storage like::

    STATICFILES_STORAGE = 'some.path.StaticStorage'
    STATIC_DJAMAZING = { ... }

and the ``STATIC_DJAMAZING`` configuration would override ``DJAMAZING``
configuration for this storage.
