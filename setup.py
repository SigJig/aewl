
from setuptools import setup
from pathlib import Path

path = Path(__file__).parent.absolute()

with open(path.joinpath('README.md')) as fp:
    long_desc = fp.read()

with open(path.joinpath('requirements.txt')) as fp:
    requires = fp.read().splitlines()

setup(
    name='aewl',
    description='Extensible GUI creation language for Arma 3',
    long_description=long_desc,
    author='Sigmund "Sig" Klåpbakken',
    author_email="sigmundklaa@outlook.com",
    url='https://github.com/SigJig/armaconfig.py',
    install_requires=requires,
    license='MIT',
    version='0.1.0',
    packages=['aewl', 'aewl.models', 'aewl.defaults'],
    package_data={
        'aewl': [
            'data/grammar.lark'
        ]
    }
)
