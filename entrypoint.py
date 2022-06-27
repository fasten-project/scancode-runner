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
import argparse
import pprint
from runner.plugin import Plugin
from runner.config import Config
from runner.scancode import ScanCodeRunner


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

tool_name = 'ScanCode Runner'
tool_description = 'A FASTEN plug-in that runs ScanCode Toolkit on a code base.'
tool_version = '0.0.1'


def get_args_parser():
    args_parser = argparse.ArgumentParser("ScanCode Runner")

    args_parser.add_argument('--input_dir', type=str,
                             default=None,
                             help="Run code analysis on specified directory. Will not connect to Kafka when specified.")

    args_parser.add_argument('--output_dir', type=str,
                             default='.',
                             help="Directory to output the results of code analysis.")

    args_parser.add_argument('--extensions', type=str, 
                             nargs='*',
                             help="List of file name extensions that should be analysed. If unspecified, all files will be scanned.")

    args_parser.add_argument('--consume_topic', type=str,
                             default='fasten.SourcesProvider.out',
                             help="Kafka topic to consume from.")

    args_parser.add_argument('--produce_topic', type=str,
                             default='fasten.ScanCodeRunner.out',
                             help="Kafka topic to produce product-level messages to.")

    args_parser.add_argument('--err_topic', type=str,
                             default='fasten.ScanCodeRunner.err',
                             help="Kafka topic to write errors to.")

    args_parser.add_argument('--log_topic', type=str,
                             default='fasten.ScanCodeRunner.log',
                             help="Kafka topic to write logs to.")

    args_parser.add_argument('--bootstrap_servers', type=str,
                             default='localhost',
                             help="Kafka servers, comma separated list between quotes.")

    args_parser.add_argument('--group_id', type=str,
                             default='ScanCodeRunner',
                             help="Kafka consumer group ID to which the consumer belongs.")

    args_parser.add_argument('--consumer_timeout_ms', type=int,
                             default=1000,
                             help="Timeout in milliseconds to consume messages from topic.")

    args_parser.add_argument('--consumption_delay_sec', type=int,
                             default=1,
                             help="Delay in seconds between each message consumption call.")

    args_parser.add_argument('--max_log_message_width', type=int,
                             default=1024,
                             help="Maximum number of characters before a log message will be truncated.")

    return args_parser


def get_config(args):
    c = Config('Default')
    c.add_config_value('input_dir', args.input_dir)
    c.add_config_value('output_dir', args.output_dir)
    c.add_config_value('extensions', args.extensions)
    c.add_config_value('bootstrap_servers', args.bootstrap_servers)
    c.add_config_value('consume_topic', args.consume_topic)
    c.add_config_value('produce_topic', args.produce_topic)
    c.add_config_value('err_topic', args.err_topic)
    c.add_config_value('log_topic', args.log_topic)
    c.add_config_value('group_id', args.group_id)
    c.add_config_value('consumption_delay_sec', args.consumption_delay_sec)
    c.add_config_value('consumer_timeout_ms', args.consumer_timeout_ms)
    c.add_config_value('max_log_message_width', args.max_log_message_width)
    return c


def main():
    parser = get_args_parser()
    config = get_config(parser.parse_args())

    logger.info(tool_name + ' ' + tool_version)
    logger.info('Running with configuration ' +
                '\"' + config.get_config_name() + '\"')

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(config.get_all_values())

    if(config.get_config_value('input_dir') != None):
        run_cli(config)
    else:
        run_kafka_plugin(config)


def run_kafka_plugin(config):
    logger.info('Creating Kafka plugin... ')
    plugin = Plugin(tool_name, tool_version,
                    tool_description, config)
    plugin.run_forever()


def run_cli(config):
    logger.info('Running without Kafka connection on input directory: ' + config.get_config_value('input_dir'))
    runner = ScanCodeRunner(config.get_config_value('extensions'))
    result_dir = runner.analyze(config.get_config_value('input_dir'), config.get_config_value("output_dir"))


if __name__ == "__main__":
    main()
