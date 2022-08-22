#  Author: Andrii Malchyk
#  mail: snooki17@gmail.com
#  Licensed under the MIT License
#  Copyright (c) 2022.
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

with open('README.md') as f:
    readme = f.read()

setup(name='rss_reader',
      version='2.0',
      description='Pure Python command-line RSS reader',
      long_description=readme,
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
      ],
      url='https://git.epam.com/andrii_malchyk/rss_reader',
      author='Andrii Malchyk',
      author_email='snooki17@gmail.com',
      license='MIT',
      packages=find_packages(),
      entry_points={
          'console_scripts': ['rss_reader=rss_reader.rss_reader:main']
      },
      install_requires=requirements,
      zip_safe=False)
