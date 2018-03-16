from setuptools import setup, find_packages

setup(name='AnkiTools',
      version='0.1.5',
      description='Anki *.apkg reader in a human-readable format; and an editor.',
      url='https://github.com/patarapolw/AnkiTools',
      author='Pacharapol Withayasakpunt',
      author_email='patarapolw@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['test']),
      install_requires=['requests'],
      python_requires='>=2.7'
      )
