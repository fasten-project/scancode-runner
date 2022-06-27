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
import pytest
from runner.scancode import ScanCodeRunner


@pytest.fixture(scope='session')
def runner(output_dir, temp_dir):
    yield ScanCodeRunner(None)


def test_pass(runner, input_dir, output_dir, temp_dir):
    pass


def test_smoke(runner, input_dir, output_dir, temp_dir):
    result = runner.analyze(os.path.join(input_dir, 'maven', 'm1'),
                            os.path.join(output_dir, 'maven', 'm1'))
    print(result)
    pass
