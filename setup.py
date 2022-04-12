import os.path

from setuptools import find_packages, setup

from pyage import __version__


# although fairly straight forward
# grabbed that one from Cython
def dev_status(version: str) -> str:
    if "b" in version or "c" in version:
        # 1b1, 1beta1, 2rc1, ...
        return "Development Status :: 4 - Beta"
    elif "a" in version:
        # 1a1, 1alpha1, ...
        return "Development Status :: 3 - Alpha"
    else:
        return "Development Status :: 5 - Production/Stable"


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
        "dev": dev_requirements.splitlines()[1:],
    },
    license="GNU GPL v3",
    classifiers=[
        dev_status(__version__),
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: pygame",
    ],
)
