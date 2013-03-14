import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

versionfile = open("pennywise/_version.py", "rt").read()
mo = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", versionfile, re.M)
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in pennywise/_version.py.")

requires = [
    'nodular',
    'SQLAlchemy>=0.8',
    ]

setup(name='pennywise',
    version=version,
    description='Double-entry accounting library.',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
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
    url='https://github.com/jace/pennywise',
    keywords='accounting',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='pennywise',
    install_requires=requires,
    )
