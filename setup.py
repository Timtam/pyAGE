import os.path

from setuptools import find_packages, setup

from pyage import __version__

requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")

with open(requirements_file, "r") as f:
    requirements = f.read()

dev_requirements_file = os.path.join(os.path.dirname(__file__), "requirements-dev.txt")

with open(dev_requirements_file, "r") as f:
    dev_requirements = f.read()

setup(
    name="python-pyage",
    version=__version__,
    author="Toni Barth",
    author_email="software@satoprogs.de",
    url="https://github.com/Timtam/pyAGE",
    packages=find_packages(),
    package_data={
        "pyage": ["py.typed"],
    },
    install_requires=requirements.splitlines(),
    extras_require={
        "ao2": [
            "accessible_output2 @ git+https://github.com/accessibleapps/accessible_output2@327bdea5e0a079bc507e341c1cb4631206675a2d#egg=accessible_output2",
        ],
        "dev": dev_requirements.splitlines()[1:],
    },
)
