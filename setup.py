import os
from setuptools import setup, find_packages
import pennywise

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'Flask',
    'Flask-SQLAlchemy',
    'SQLAlchemy>=0.6',
    ]

setup(name='pennywise',
      version=pennywise.__version__,
      description='Web-based double-entry accounting server.',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: JavaScript",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Office/Business :: Financial :: Accounting",
        ],
      author='Kiran Jonnalagadda',
      author_email='jace@pobox.com',
      url='http://jace.github.com/pennywise',
      keywords='accounting',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='pennywise',
      install_requires=requires,
      )
