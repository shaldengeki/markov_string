try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

config = {
  'description': 'markov string generator', 
  'author': 'Shal Dengeki', 
  'url': 'https://github.com/shaldengeki/markov_string', 
  'download_url': '', 
  'author_email': 'shaldengeki@gmail.com', 
  'version': '0.1', 
  'install_requires': ['nose'], 
  'packages': [], 
  'scripts': [],
  'name': 'markov_string'
}

setup(**config)