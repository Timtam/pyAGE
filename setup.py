from setuptools import find_packages, setup

setup(
    name="pyAGE",
    version="0.1",
    author="Toni Barth",
    author_email="software@satoprogs.de",
    url="https://github.com/Timtam/pyAGE",
    packages=find_packages(),
    setup_requires=[
        "flake8",
    ],
    install_requires=[
        "cytolk==0.1.3",
        "pygame==2.0.0-dev12",
        "synthizer==0.7.3",
    ],
)
