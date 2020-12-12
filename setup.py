import setuptools
from setuptools import Extension
#from distutils.core import setup, Extension

_oodle = Extension('oodle._oodle',
                    define_macros = [],
                    include_dirs = ['/usr/local/include'],
                    libraries = ['liboodle_static'],
                    library_dirs = ['/usr/local/lib'],
                    sources = ['_swizzle.cpp'],
                    extra_compile_args=["-O2 "])

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oodle",
    version="0.0.1",
    author="Emelia",
    author_email="2634959+baconwaifu@users.noreply.github.com",
    description="LibOodle Wrapper for Python3.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/baconwaifu/python_oodle",
    packages=["oodle"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: System :: Archiving :: Compression",
    ],
    python_requires='>=3.4',
    ext_modules=[],
    zip_safe = True
)

