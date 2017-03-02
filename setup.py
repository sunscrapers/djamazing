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
    requires=[
        'django_threadlocals',
    ]
)
