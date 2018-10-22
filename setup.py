from setuptools import setup

setup(
        name='haf',
        version='1.0.4',
        description=(
            '''
            haf : http api auto test framework
            
            pip install haf --upgrade

            python -m haf'''
        ),
        url='http://github.com/tsbxmw/haf',
        packages=['haf'],
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