from setuptools import setup, find_packages


setup(
    name="docker-remote-sync",
    version="0.1.5",
    packages=find_packages(),
    entry_points={"console_scripts": ["drsync=drsync.drsync:main"]},
)
