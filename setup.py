from setuptools import setup, find_packages

setup(
    name='actuaviz',
    version='1.0',
    author='yoyo',
    author_email='fdtrretvx342242@gmail.com',
    description='Coding when being an intern in ActuaViz, 2022 summer',
    packages=find_packages(),
    scripts=['bin/EL.py','bin/Premium.py','bin/Reserve.py'],
    install_requires=['numpy==1.22.0','pandas','PyMySQL==1.0.2','requests','sshtunnel==0.4.0',' xlwings==0.24.9']
)