from setuptools import setup, find_packages

setup(
    name="civicguardian",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "boto3>=1.28.0",
        "pytest>=7.0.0",
        "hypothesis>=6.0.0",
    ],
)
