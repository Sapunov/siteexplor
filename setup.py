"""Sitexplor installation script."""

from __future__ import unicode_literals

from setuptools import find_packages, setup

if __name__ == "__main__":
    with open("README") as readme:
        setup(
            name="sitexplor",
            version="0.2",

            description=readme.readline().strip(),
            long_description=readme.read().strip() or None,
            url="https://github.com/Sapunov/sitexplor",

            license="GPL3",
            author="Nikita Sapunov",
            author_email="kiton1994@gmail.com",

            classifiers=[
                "Intended Audience :: Operations",
                "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                "Operating System :: MacOS :: MacOS X",
                "Operating System :: POSIX",
                "Operating System :: Unix",
                "Programming Language :: Python :: 2"
            ],
            platforms=["unix", "linux", "osx"],

            install_requires=["psh", "requests", "bs4"],
            packages=find_packages(),
        )
