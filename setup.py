from distutils.core import setup

setup(name='ComplexAutomatonBase',
      version='0.9',
      description='Framework for Combined CAs and ABMs',
      author='Michael Wagner',
      author_email='wagner.mchl@googlemail.com',
      url='https://github.com/micutio/ComplexAutomatonBase',
      packages=['cab', 'cab/abm', 'cab/ca', 'cab/util'], requires=['pygame']
      )