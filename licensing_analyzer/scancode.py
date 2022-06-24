# Copyright 2022 Software Improvement Group
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging
import datetime

from licensing_analyzer.utils import Utils

logger = logging.getLogger(__name__)


class ScancodeRunner:

    def __init__(self, base_dir):
        self.analyzer_name = "Scancode Toolkit"
        self.base_dir = base_dir

    def analyze(self, payload):
        out_payload = {}
        return out_payload
