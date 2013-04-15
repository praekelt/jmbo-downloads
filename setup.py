from setuptools import setup, find_packages

setup(
    name='jmbo-downloads',
    version='0.0.6',
    description='Downloads for Jmbo.',
    long_description=(open('README.rst', 'r').read() +
                        open('AUTHORS.rst', 'r').read() +
                        open('CHANGELOG.rst', 'r').read()),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/jmbo-downloads',
    packages = find_packages(),
    install_requires = [
        'jmbo>=0.1.20'
    ],
    include_package_data=True,
    tests_require=[
        'jmbo>=1.0',
        'django-setuptest',
        'coverage',
    ],
    test_suite="setuptest.setuptest.SetupTestSuite",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
