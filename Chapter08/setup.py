#!/usr/bin/env python
from distutils.core import setup, Extension
MOD = 'CCollision'
setup(name=MOD, ext_modules=[Extension(MOD, sources=['CCollision.c'])])