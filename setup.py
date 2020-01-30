import setuptools


with open('README.md') as f:
    long_description = f.read()


setuptools.setup(
    name='PyMyModules',
    version='0.0.1',
    author='Brent Jeffson Florendo',
    author_email='brentjeffson@gmail.com',
    description='Collection of Modules for Scripting',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/brentjeffson/PyMyModules'
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)