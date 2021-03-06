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
import scancode_config
from pathlib import PurePath
from datetime import datetime, timezone

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ScanCodeRunner:

    def __init__(self, extensions):
        self.analyzer_name = "ScanCode Toolkit"
        self.analyzer_version = scancode_config.__version__
        if extensions is not None:
            self.extensions = tuple(extensions)
        else:
            self.extensions = tuple()

    def analyze(self, input_dir, output_dir):
        results = {'analyzer_name': self.analyzer_name,
                   'analyzer_version': self.analyzer_version,
                   'analysis_timestamp': datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S%Z"),
                   'analysis_working_dir': os.getcwd(),
                   'analysis_input_dir': input_dir,
                   'analysis_output_dir': output_dir}
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
                abs_file = os.path.join(root, name)
                rel_file = self.make_file_relative_to(abs_file, input_dir)
                if not self.skip_file(abs_file):
                    logger.info("Scanning " + rel_file)
                    scan_result = scancode.api.get_licenses(abs_file)
                    file_licenses.update({rel_file:
                                          self.select_file_licenses_output(scan_result)})
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

    def skip_file(self, file):
        if self.extensions is not tuple():
            if not file.endswith(self.extensions):
                return True
        else:
            prog_lang = scancode.api.get_file_info(file)['programming_language']
            if prog_lang is None or prog_lang == '':
                return True
        return False
