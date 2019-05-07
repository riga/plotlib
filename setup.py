# coding: utf-8


import os
from setuptools import setup, find_packages

import plotlib as pl


this_dir = os.path.dirname(os.path.abspath(__file__))


keywords = [
    "physics", "analysis", "plotting", "root", "matplotlib",
]


classifiers = [
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Development Status :: 4 - Beta",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: BSD License",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Information Technology",
]


# read the readme file
with open(os.path.join(this_dir, "README.md"), "r") as f:
    long_description = f.read()


# load installation requirements
with open(os.path.join(this_dir, "requirements.txt"), "r") as f:
    install_requires = [line.strip() for line in f.readlines() if line.strip()]


setup(
    name=pl.__name__,
    version=pl.__version__,
    author=pl.__author__,
    author_email=pl.__email__,
    description=pl.__doc__.strip().split("\n")[0].strip(),
    license=pl.__license__,
    url=pl.__contact__,
    keywords=keywords,
    classifiers=classifiers,
    long_description=long_description,
    install_requires=install_requires,
    python_requires=">=2.7",
    zip_safe=False,
    packages=find_packages(exclude=["tests"]),
)
