from setuptools import setup, find_packages

setup(
    name='ece576',
    version='0.1',
    packages=find_packages(include=['src*', 'utility*']),
)
