from setuptools import setup, find_packages
from _version import __version__

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name="croctalk",
    version=__version__,
    packages=find_packages(),
    install_requires=install_requires,
    scripts=['_version.py'],
    entry_points={
        'console_scripts': [
            'croctalk = croctalk.main:main',  # Adjust this line if your main function is elsewhere
        ],
    },
)

