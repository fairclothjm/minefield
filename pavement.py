#!/usr/bin/python

from paver.easy import *
#from paver.setuputils import setup
import paver.doctools
import os
import glob
import shutil


@task
def setup():
    sh('python3 setup.py -q install')
    pass

@task
def test():
  sh('nosetests --with-coverage test')
  pass

@task
def clean():
  for pycfile in glob.glob("*/*/*.pyc"): os.remove(pycfile)
  for pycache in glob.glob("*/__pycache__"): os.removedirs(pycache)
  for pycache in glob.glob("./__pycache__"): shutil.rmtree(pycache)
  pass

@task
@needs(['setup', 'test', 'clean'])
def default():
  pass

@task
def run():
  sh('python3 src/minegui.py')
  pass
