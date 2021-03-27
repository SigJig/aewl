
from setuptools import setup
from pathlib import Path

path = Path(__file__).parent.absolute()

setup(
    name='aewl',
    description='Extensible GUI creation language for Arma 3',
    author='Sigmund "Sig" Klåpbakken',
    author_email="sigmundklaa@outlook.com",
    url='https://github.com/SigJig/armaconfig.py',
    license='MIT',
    version='0.1.0',
    packages=['aewl'],
    package_data={
        'aewl': [
            'data/base.hpp', 'data/grammar.lark'
        ]
    }
)