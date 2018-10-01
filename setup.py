import os
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('requirements.txt') as requirements_file:
    REQUIREMENTS = [line.rstrip() for line in requirements_file if line != '\n']

with open('apiron/VERSION') as version_file:
    VERSION = version_file.readlines()[0].strip()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='apiron',
    version=VERSION,
    author='Ithaka Harbors, Inc.',
    author_email='grp_ithaka_apiron@ithaka.org',
    url='https://github.com/ithaka/apiron',
    license='MIT',

    description='apiron helps you cook a tasty client for RESTful APIs. Just don\'t wash it with SOAP.',
    long_description=README,
    long_description_content_type='text/markdown',

    packages=find_packages(),
    include_package_data=True,

    install_requires=REQUIREMENTS,

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
    ],
)
