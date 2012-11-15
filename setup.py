#!/usr/bin/env python

from distutils.core import setup
import collector

setup(name='netflowinterface',
      version=collector.__version__,
      author=collector.__author__,
      url=collector.__url__,
      description='netflow interface module',
      packages=[ 'netflowinterface' ])