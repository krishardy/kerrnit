import os
import fnmatch

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

install_requires = []
dependency_links = []

def parse_requirements(path):
    return [line.strip() for line in open(path) if line and line.startswith('#') is False]

requirements = parse_requirements(
    'requirements.txt'
)

for item in requirements:
    install_requires.append(item)

# Lookup the version from the code
version = '0.1'

EXCLUDE_FROM_PACKAGES = []

package_data_paths = {
}

package_data = {}

for package_name in package_data_paths:
    if package_name not in package_data:
        package_data[package_name] = []
    for data_dir in package_data_paths[package_name]:
        package_data[package_name].extend(
            [os.path.join(dirpath, f)[len(package_name)+1:]
             for dirpath, dirnames, files in os.walk(os.path.join(package_name, data_dir))
             for f in fnmatch.filter(files, '*')])

setup(
    name='kerrnit',
    version=version,
    url='http://github.com/krishardy/kerrnit/',
    author='Kris Hardy',
    author_email='kris@rkrishardy.com',
    description=('Replacement string generator for kern-confusable string'),
    license='Apache Software License',
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    package_data=package_data,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'kerrnit = kerrnit:main'
        ]
    },
    extras_require={
    },
    install_requires=install_requires,
    dependency_links=dependency_links,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    download_url=''
)
