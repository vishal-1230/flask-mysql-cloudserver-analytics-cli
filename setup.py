# setup.py
from setuptools import setup, find_packages

setup(
    name='flask-mysql-analytics',
    version='1.0',
    packages=find_packages(),
    long_description="Test desc",
    install_requires=[
        "paramiko",
        "argparse",
    ],
    entry_points={
        'console_scripts': [
            'server=flaskmysqlanalytics.main:start',
        ],
    },
)
