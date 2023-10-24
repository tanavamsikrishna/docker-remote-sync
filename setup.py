from setuptools import setup, find_packages


setup(
    name="docker-remote-sync",
    version="0.1.2",
    packages=find_packages(),
    entry_points={"console_scripts": ["drsync = drsync.__main__:main"]},
)
