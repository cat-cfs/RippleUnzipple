from setuptools import setup, find_packages

setup(
    name='RippleUnzipple',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'py7zr==0.20.8',
        # Add any other dependencies here
    ],
)
