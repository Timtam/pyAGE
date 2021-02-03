import os.path

from setuptools import find_packages, setup

from pyage import __version__

requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")

with open(requirements_file, "r") as f:
    requirements = f.read()

setup(
    name="pyAGE",
    version=__version__,
    author="Toni Barth",
    author_email="software@satoprogs.de",
    url="https://github.com/Timtam/pyAGE",
    packages=find_packages(),
    install_requires=requirements.split("\r\n"),
)
