import setuptools, os
from setuptools import setup

PACKAGE_NAME = "haf"


with open('ReadMe.md', encoding='utf8') as f:
    long_description = f.read()


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


package_extras = []
package_extras.extend(package_files('{}/bin/allure'.format(PACKAGE_NAME)))
package_extras.extend(package_files('{}/check'.format(PACKAGE_NAME)))
package_extras.extend(package_files('{}/codegenerator'.format(PACKAGE_NAME)))
package_extras.extend(package_files('{}/pylib'.format(PACKAGE_NAME)))
package_extras.extend(package_files('{}/setup'.format(PACKAGE_NAME)))
package_extras.extend(package_files('{}/testcase'.format(PACKAGE_NAME)))


setup(
        name = 'haf',
        version = '1.0.5',
        author = 'wei.meng',
        author_email = 'mengwei1101@hotmail.com',
        long_description_content_type='text/markdown',        
        long_description = long_description,

        url='http://github.com/tsbxmw/haf',

        packages = setuptools.find_packages(exclude=['testcases','thirdparty']),
        package_data = {"": package_extras},
        install_requires=[
            'pytest',
            #pytest-allure-adaptor
            'allure-pytest',
            'requests',
            'openpyxl',
            'pymysql',
            #export PYMSSQL_BUILD_WITH_BUNDLED_FREETDS=1
            #pymssql
            'sphinx',
            'xpinyin',
            'paramiko',
            'pytest-html',
            'redis'
        ]
)