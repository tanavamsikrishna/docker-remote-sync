from setuptools import setup, find_packages


setup(
    name="docker-remote-sync",
    version="0.1.0",
    packages=find_packages(),
    entry_points={"console_scripts": ["drsync = docker-remote-sync.__main__:main"]},
)
