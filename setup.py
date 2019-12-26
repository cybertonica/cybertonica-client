from setuptools import setup
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='CybertonicaAPI',
      version='0.1',
      description='Python client for the Cybertonica Open API',
      url='https://apogee:mksuhAe2cD_ZMT1pdLCA@gitlab.cybertonica.com/ochaplashkin/openapi_python_client.git',
      author='Cybertonica Ltd.',
      author_email='support@cybertonica.com',
      license='unlicense',
      packages=['CybertonicaAPI'],
      install_requires=['requests'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False,
      classifiers=[  
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    	]
)