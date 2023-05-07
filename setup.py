import os

from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "requirements.txt")) as fd:
    requirements = fd.read()
    install_requires = [r.strip() for r in requirements.split('\n') if r.strip()]

extras_require = {
    "dev": [
        'flake8',
        'flake8-bugbear>=21.11.28',
        'flake8-mutable',
        'flake8-print',
        'flake8-return',
        'mccabe',
        'pep8-naming',
        'pytest-cov>=3.0.0',
        'pytest-flask>=1.2.0',
        'pytest-spec>=3.2.0',
        'pytest>=6.2.5',
    ]
}

setup(
    name='splendor',
    version='1.0.0',
    python_requires='>=3.10',
    include_package_data=True,
    package_data={},
    packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
    install_requires=install_requires,
    extras_require=extras_require,
)
