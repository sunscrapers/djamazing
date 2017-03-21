import base64
import datetime
import hashlib
import mimetypes

import boto3
from botocore.signers import CloudFrontSigner
from botocore.client import Config
from botocore.exceptions import ClientError
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import Storage
from django.core.signing import Signer, BadSignature
from threadlocals.threadlocals import get_current_user 


SIGNER = Signer()


def get_signature(filename, username):
    signature = SIGNER.sign(':'.join([filename, username]))
    return signature.rsplit(':', 1)[1]


def check_signature(signature, filename, username):
    try:
        SIGNER.unsign(':'.join([filename, username, signature]))
    except BadSignature:
        return False
    return True


class S3File(object):
    def __init__(self, name, s3_object):
        self.name = name
        self.data = s3_object.get()

    @property
    def size(self):
        return self.data['ContentLength']

    @property
    def file(self):
        return self

    @property
    def open(self):
        return self

    def read(self, num_bytes=None):
        return self.data['Body'].read(num_bytes)

    def chunks(self, chunk_size=None):
        while True:
            chunk = self.read(chunk_size)
            if chunk:
                yield chunk
            else:
                return

    def __iter__(self):
        for chunk in self.chunks():
            for line in chunk.split('\n'):
                yield line


class DjamazingStorage(Storage):

    def __init__(self, config=None):
        config = config or settings.DJAMAZING
        self.view_base_url = '/djamazing'
        self.cloud_front_base_url = config['CLOUDFRONT_URL']
        self.bucket = boto3.resource(
            's3',
            aws_access_key_id = config['S3_KEY_ID'],
            aws_secret_access_key = config['S3_SECRET_KEY'],
            config=Config(signature_version='s3v4')
        ).Bucket(config['S3_BUCKET'])
        self._init_protected_mode(config)

    def _init_protected_mode(self, config):
        self.protected = 'CLOUDFRONT_KEY_ID' in config
        if self.protected:
            cloud_front_key = self._get_cloud_front_key(config)
            self.key_id = config['CLOUDFRONT_KEY_ID']
            self.cloud_front_key = serialization.load_pem_private_key(
                cloud_front_key,
                password=None,
                backend=default_backend(),
            )
            self.signer = CloudFrontSigner(self.key_id, self.rsa_signer)

    def _get_cloud_front_key(self, config):
        cloud_front_key = config.get('CLOUDFRONT_KEY')
        cloud_front_key_file = config.get('CLOUDFRONT_KEY_FILE')
        if not cloud_front_key and cloud_front_key_file:
            with open(cloud_front_key_file, 'br') as f:
                cloud_front_key = f.read()
        if not cloud_front_key:
            raise ImproperlyConfigured(
                'Either of CLOUDFRONT_KEY'
                ' or CLOUDFRONT_KEY_FILE should be configured'
            )
        return cloud_front_key

    def url(self, filename):
        if self.protected:
            user = get_current_user().get_username()
            signature = get_signature(filename, user)
            return '{}/{}/?signature={}'.format(
                self.view_base_url,
                filename,
                signature,
            )
        else:
            return self.cloud_front_base_url + filename

    def delete(self, filename):
        self.bucket.delete_objects(Delete={'Objects': [{'Key': filename}]})

    def exists(self, filename):
        try:
            self.bucket.Object(filename).get()
        except ClientError:
            return False
        return True

    def _open(self, filename, mode='rb'):
        if mode != 'rb':
            raise ValueError('Unsupported mode')
        object_ = self.bucket.Object(filename)
        return S3File(filename, object_)

    def _save(self, filename, content):
        hash_ = hashlib.md5()
        for chunk in content.chunks():
            hash_.update(chunk)
        md5 = base64.b64encode(hash_.digest()).decode('ascii')
        content.seek(0)
        mime, _ = mimetypes.guess_type(filename)
        mime = mime or 'application/octet-stream'
        ACL = 'private' if self.protected else 'public-read'
        self.bucket.put_object(
            ACL='private',
            Body=content,
            Key=filename,
            ContentType=mime,
            ContentMD5=md5,
        )
        return filename

    def rsa_signer(self, data):
        signer = self.cloud_front_key.signer(padding.PKCS1v15(), hashes.SHA1())
        signer.update(data)
        return signer.finalize()

    def cloud_front_url(self, filename):
        expiration_time = (
            datetime.datetime.now() +
            datetime.timedelta(seconds=1)
        )
        url = self.cloud_front_base_url + filename
        return self.signer.generate_presigned_url(
            url,
            date_less_than=expiration_time,
        )
