from setuptools import setup

setup(
    name='analysis',
    version='0.1.0',
    author='Analysis Team',
    packages=['analysis'],
    install_requires=[
        'matplotlib',
        'PyYAML',
        'requests',
        'pytest',
        'logging'
    ]
)
