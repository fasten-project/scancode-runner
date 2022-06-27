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
#

import os
import shutil
import pytest


@pytest.fixture(scope='session')
def input_dir(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("input_dir")
    shutil.copytree('runner/tests/resources', tmp, dirs_exist_ok=True)
    yield tmp


@pytest.fixture(scope='session')
def output_dir(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("output_dir")
    yield tmp


@pytest.fixture(scope='session')
def temp_dir(tmp_path_factory):
    tmp = tmp_path_factory.mktemp("temp_dir")
    yield tmp


def fix_sourcePath(record, tmp_sources_path):
    if "sourcePath" in record:
        sourcePath = record["sourcePath"]
        record.update(
            {"sourcePath": os.path.join(tmp_sources_path, sourcePath)})
    return record
