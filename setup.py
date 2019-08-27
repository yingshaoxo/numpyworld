from setuptools import setup, Extension, find_packages
from os.path import dirname, join, abspath

file_path = join(abspath(dirname(__file__)), "README.md")
with open(file_path) as f:
    long_description = f.read()

setup(
    name='numpyworld',
    version='0.1',
    description='Use numpy to create a world that you dreamed about!',
    long_description_content_type='text/markdown',
    long_description=long_description,
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: System',
        'License :: OSI Approved :: MIT License'
    ],
    keywords='numpyworld',
    url='https://github.com/yingshaoxo/numpyworld',
    author='yingshaoxo',
    author_email='yingshaoxo@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'setuptools',
        'numpy',
        'matplotlib',
        'pillow',
    ]
)
