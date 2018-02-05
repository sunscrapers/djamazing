from setuptools import setup, find_packages

with open('README.rst') as f:
    description = f.read()


setup(
    name="djamazing",
    version='0.1.0',
    packages=find_packages(),
    license='MIT',
    author='SUNSCRAPERS',
    author_email='info@sunscrapers.com',
    description='Safe storage for django using AWS S3+CloudFront',
    long_description=description,
    url='https://github.com/sunscrapers/djamazing',
    install_requires=[
        'boto3>=1.4.4',
        'cryptography>=1.7.2',
        'django-threadlocals>=0.8',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications :: File Sharing',
    ],
)
