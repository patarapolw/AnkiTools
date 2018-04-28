from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='AnkiTools',
    version='0.1.9',
    description='Anki *.apkg reader in a human-readable format; and an editor',
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/patarapolw/AnkiTools',
    author='Pacharapol Withayasakpunt',
    author_email='patarapolw@gmail.com',
    license='MIT',
    keywords='Anki AnkiConnect',  # Optional
    packages=find_packages(exclude=['test']),
    install_requires=['requests', 'openpyxl'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities'
    ],
    python_requires='>=3',
    tests_require=['pytest'],
    extras_require={
        'tests': ['pytest']
    }
)
