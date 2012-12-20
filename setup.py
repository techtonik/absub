#!/usr/bin/env python

from distutils.core import setup

long_description = "Cross-platform wrapper around subprocess.Popen to provide "
long_description += "an asynchronous version of Popen.communicate()."


def get_version(relpath):
    """read version info from file without importing it"""
    from os.path import dirname, join
    for line in open(join(dirname(__file__), relpath)):
        if '__version__' in line:
            if '"' in line:
                # __version__ = "0.9"
                return line.split('"')[1]
            elif "'" in line:
                return line.split("'")[1]

setup(name='async_subprocess',
      version=get_version('async_subprocess.py'),
      description="Asynchronous subprocess.Popen module",
      long_description=long_description,
      author="James Buchwald",
      author_email="buchwj@rpi.edu",
      url="http://pypi.python.org/pypi/async_subprocess/",
      provides=['async_subprocess'],
      
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          ],
      
      py_modules=['async_subprocess'],
      data_files=[('', ['LICENSE'])],
)
