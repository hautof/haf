import setuptools, os
from setuptools import setup

PACKAGE_NAME = "haf"

requires = [
            'pytest',
            'allure-pytest',
            'requests',
            'openpyxl',
            'pymysql',
            'sphinx',
            'xpinyin',
            'paramiko',
            'pytest-html',
            'redis',
            'assertpy'
        ]

with open('ReadMe.md', encoding='utf8') as f:
    long_description = f.read()


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


package_extras = []


package_extras.extend(package_files('{}/bin'.format(PACKAGE_NAME)))
package_extras.extend(package_files('{}/pylib'.format(PACKAGE_NAME)))
package_extras.extend(package_files('{}/codegenerator'.format(PACKAGE_NAME)))
package_extras.extend(package_files('{}/setup'.format(PACKAGE_NAME)))
package_extras.extend(package_files('{}/testcase'.format(PACKAGE_NAME)))
package_extras.extend(package_files('{}/check'.format(PACKAGE_NAME)))


setup(
    name = 'haf',
    version = '1.1.5',
    author = 'wei.meng',
    author_email = 'mengwei1101@hotmail.com',    
    long_description = long_description,
    long_description_content_type='text/markdown',

    url='http://github.com/tsbxmw/haf',

    packages = setuptools.find_packages(exclude=['testcases','thirdparty']),
    package_data = {"": package_extras},
    python_requires='>=3.5.2',
    install_requires=requires,
    platforms='Posix; MacOS X; Windows',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)