try: 
    from setuptools import setup
    from setuptools import Extension
    from Cython.Build import cythonize
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension
    from Cython.Build import cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="fmup",
    version="1.5.10.0",
    author="iammix",
    url="https://github.com/redi-eng",
    description="Python Framework that builds FMU files from Python Source Code",
    long_description_content_type="text/markdown",
    keywords="FMI",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering",
    ],
    python_requires='>=3.6',
)
