from tstock.settings import __version__
from setuptools import setup

setup(
    name="tstock",
    version=__version__,
    author="Gabe Banks",
    author_email="gabriel.t.banks@gmail.com",
    description="A command line tool to view stock charts in the terminal.",
    long_description="file: README.md",
    long_description_content_type="text/markdown",
    keywords="tstock stock ticker finance crypto",
    url="https://github.com/Gbox4/tstock",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent"
    ],
    packages=["tstock"],
    entry_points={"console_scripts": ["tstock=tstock.__main__:main"]},
    python_requires=">=3.6")