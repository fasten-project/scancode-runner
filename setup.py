# Copyright 2022 Software Improvement Group
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ScanCode Runner',
    version='0.0.1',
    description='Runs ScanCode Toolkit on a code base.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    author='',
    author_email='',
    classifiers=[
        'Programming Language :: Python :: 3.9',
    ],
    keywords='',
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=[
        'fasten',
        'kafka-python==2.0.2',
        'python-snappy',
        'crc32c',
        'scancode-toolkit'
    ]
)
