from setuptools import setup, find_packages

setup(
    name="sample_project",  # o el nombre de tu proyecto
    version="0.1.0",
    packages=find_packages(),  # Esto encontrará todos los paquetes que tengan __init__.py
    install_requires=[
        "pytest",
        "pytest-cov",
        "requests",
    ],
)
