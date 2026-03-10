from setuptools import setup, find_packages

requirements = ["pyyaml", "requests"]

setup(
    author="nbtm-sh",
    author_email="dog@nbtm.sh",
    description="szurubooru api wrapper for python",
    install_requires=requirements,
    packages=find_packages(include=['szurubooru_api']),
    version="0.1"
    name="szurubooru-api"
)
