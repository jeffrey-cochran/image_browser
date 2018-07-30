from distutils.core import setup
from setuptools import find_packages
from os.path import dirname, join
import pip

setup(
    name='metallography-data',
    version="0.0.1",
    description='Ultra High Carbon Steel Micrographs from CMU',
    author='Jeff Cochran',
    author_email='jcochran@equityeng.com',
    packages=find_packages(),
)
