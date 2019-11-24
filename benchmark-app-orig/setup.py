"""
setup.py for benchmark-app.

For reference see
https://packaging.python.org/guides/distributing-packages-using-setuptools/

"""
from pathlib import Path
from setuptools import setup, find_packages


HERE = Path(__file__).parent.absolute()
with (HERE / 'README.md').open('rt') as fh:
    LONG_DESCRIPTION = fh.read().strip()


# Requirements from accsoft-gui-pyqt-widgets (for reference):
# numpy~=1.16
# scipy>=1.1&&<2
# QtPy>=1.7&&<2
# pyqtgraph~=0.10.0

REQUIREMENTS: dict = {
    'core': [
        "PyQt5",
        "QtPy",
        "numpy",
        "scipy",
        "pyqtgraph"
    ],
    'test': [
        'pytest',
    ],
    'dev': [
        # 'requirement-for-development-purposes-only',
    ],
    'doc': [
        'sphinx',
    ],
}


setup(
    name='benchmark-app',
    version="0.0.1.dev0",

    author='Fabian Sorn',
    author_email='fabian.sorn@icloud.com',
    description='SHORT DESCRIPTION OF PROJECT',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='',

    packages=find_packages(),
    python_requires='>=3.6, <4',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

    install_requires=REQUIREMENTS['core'],
    extras_require={
        **REQUIREMENTS,
        # The 'dev' extra is the union of 'test' and 'doc', with an option
        # to have explicit development dependencies listed.
        'dev': [req
                for extra in ['dev', 'test', 'doc']
                for req in REQUIREMENTS.get(extra, [])],
        # The 'all' extra is the union of all requirements.
        'all': [req for reqs in REQUIREMENTS.values() for req in reqs],
    },
)
