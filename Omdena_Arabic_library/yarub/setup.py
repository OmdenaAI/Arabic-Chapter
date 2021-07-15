from setuptools import setup, find_packages
import pypandoc
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='yarub',
  version='0.1.0',
  description="This is code with Modern standard arabic training dataset",
  long_description= pypandoc.convert_file('README.md', 'rst'),
  author='Omdena',
  author_email='almastanul@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Arabic Training dataset', 
  packages=find_packages(),
  install_requires=[''])


