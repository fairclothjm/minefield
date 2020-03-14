from setuptools import setup, find_packages

setup(name='assign1',
      description='assign1',
      author='',
      version='0.1',
      packages=find_packages(),
      zip_safe=False,
      tests_require=['nose==1.3.7'],
      install_requires=['coverage==3.7.1', 'pygame==1.9.2b8'])
