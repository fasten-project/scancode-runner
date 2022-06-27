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

import os
import logging
import json
import scancode.api
from pathlib import PurePath

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ScanCodeRunner:

    def __init__(self, extensions):
        self.analyzer_name = "ScanCode Toolkit"
        if extensions is not None:
            self.extensions = tuple(extensions)
        else:
            self.extensions = tuple()

    def analyze(self, input_dir, output_dir):
        results = {}
        results.update({'file_licenses': self.scan_file_licenses(input_dir)})
        return self.output_results(results, output_dir)

    def output_results(self, results, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'scancode_results.json')
        with open(output_file, 'w', encoding="utf-8") as file:
            json.dump(results, file)
        logger.info('Analysis result was output to: ' + output_file)
        return output_file

    def scan_file_licenses(self, input_dir):
        logger.info("Starting file-license scan in " + input_dir)
        file_licenses = {}
        for root, dirs, files in os.walk(input_dir):
            for name in files:
                if self.extensions == tuple() or name.endswith(self.extensions):
                    abs_file = os.path.join(root, name)
                    rel_file = self.make_file_relative_to(abs_file, input_dir)
                    logger.info("Scanning " + rel_file)
                    scan_result = scancode.api.get_licenses(abs_file)
                    file_licenses.update({rel_file: self.select_file_licenses_output(scan_result)})
        return file_licenses

    def make_file_relative_to(self, filename, to):
        p = PurePath(filename)
        return str(p.relative_to(to))

    def select_file_licenses_output(self, scancode_result):
        detected_licenses = scancode_result['licenses']

        result = {}
        for license in detected_licenses:
            result.update({
                key: value for (key, value) in license.items()
                if key in ['name', 'spdx_license_key']
            })
        return result
