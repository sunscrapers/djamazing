-----------------------------------------------
Djamazing - a safe storage for AWS
-----------------------------------------------

Djamazing offers a way to use S3+Cloudfront as Django Storage. It has the
benefit over conventional storages, that it generates signed URLs, so only the
user who was able to display the URL is also able to access it.

AWS configuration
-------------------------

1. Create an S3 bucket.
2. Generate a keypair for the user that can access the bucket.
3. Create a cloudfront distribution that has origin in the bucket and is
   restricted to signed URLs.
4. Generate a cloudfront keypair that can be used in the distribution.

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
4. Add threadlocals middleware
   ``'threadlocals.middleware.ThreadLocalMiddleware'`` to your ``MIDDLEWARE``
5. Add djamazing URLs to ``urls.py``::

    url(r'^djamazing/', include(djamazing.urls)),

How does it work?
---------------

Djamazing uses two kinds of signed URL-s. 

1. The "django URLs" are signed using the ``SECRET_KEY`` in django.  They are
   signed for the currently logged in user.  It is *up to the developer* to
   make sure that only users that are meant to see the file get the ``.url()``
   method called when logged in.
2. The CloudFront URLs are created when user tries to visit the generated URL
   mentioned above. This URL is only valid for a second and it is a direct link
   to the CloudFront service.


