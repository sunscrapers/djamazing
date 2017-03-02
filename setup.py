from setuptools import setup, find_packages

with open('README.rst') as f:
    description = f.read()


setup(
    name="djamazing",
    version='0.0.1',
    packages=find_packages(),
    license='MIT',
    author='SUNSCRAPERS',
    description='Safe storage for django using AWS S3+CloudFront',
    long_description=description,
    install_requires=[
        'boto3>=1.4.4',
        'cryptography>=1.7.2',
        'django-threadlocals>=0.8',
    ],
)
