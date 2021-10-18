# app.py

import argparse
import configparser
import json
import logging
import os
from datetime import datetime

from mintmap import __version__
from mintmap.common.argument_parser import ArgumentParser
from mintmap.helpers import used_arguments_str
from mintmap.pipeline import Pipeline


class AppMetaClass(type):

    def _todo(self):
        return False


logger = logging.getLogger('app')


class App(metaclass=AppMetaClass):

    def __init__(self):
        self.custom_rpm = None
        self.parse_arguments()
        self.parse_mapping_bundle_config()

    @property
    def config(self):
        '''return instance variables as a dict'''

        return self.__dict__

    def parse_arguments(self):
        #TODO: change to pathlib
        package_path = os.path.dirname(__file__)
        default_mapping_bundle_path = os.path.join(
            package_path,
            'mappingbundle',
            #'GRCh37_FromOriginalPublication',
            'v2',
        )

        description = (
            f"MINTmap {__version__}"
            ' generates tRF (tRNA fragment) profiles '
            'from a trimmed short RNA-Seq dataset.'
        )

        parser = ArgumentParser(
            description=description,
            allow_abbrev=False,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
        parser.add_argument(
            'input_file_path',
            type=str,
            help='''
                The input_file_path contains the
                sequenced reads to be analyzed. Any
                trimming (e.g. quality and adapter trimming) must be done
                prior to running this tool. If input_file_path ends in .gz
                it will be treated as a gzipped FASTQ file.
                The FASTQ file contains four lines per read (more info
                here: https://en.wikipedia.org/wiki/FASTQ_format).
                Color-space reads are not supported.
                This is a required argument.
            '''
        )

        parser.add_argument(
            '-c',
            '--custom-rpm',
            default=None,
            dest='custom_rpm',
            type=int,
            help='''
                The value CUSTOM_RPM is meant to be used as alternative
                denominator when computing the rpm abundance of an isomir.
                When this parameter is defined by the user, an additional
                column in the output files will be populated with rpm values
                that have been calculated using this value in the
                denominator - i.e. these values will be equal to raw
                reads/<customrpm>*1,000,000, a common value to use here is
                the original number of sequenced reads prior to quality
                and adaptor-trimming.
            '''
        )

        parser.add_argument(
            '-m',
            '--mapping-bundle',
            default=default_mapping_bundle_path,
            dest='mapping_bundle_path',
            type=str,
            help=f'''
                This is the relative or
                absolute path to the mapping bundle that will be used.
                If not specified, mapping bundle path is set to
                {default_mapping_bundle_path}
            '''
        )

        parser.add_argument(
            '-p',
            '--prefix',
            default='output',
            dest='prefix',
            type=str,
            help='''
                Naming prefix for the generated files.
                If not specified, OUTPUT_PREFIX will be set to "output" and all
                output files will be generated in the current working directory.
            '''
        )

        parser.add_argument(
            "--log-level",
            default='info',
            dest="log_level",
            choices=['debug',
                     'info',
                     'warning',
                     'error',
                     'critical'],
            metavar='{debug,info,warning}',  # show less options for readability
            help="Set the logging level. The default is info.",
        )

        parser.add_argument(
            '--version',
            action='version',
            version=__version__,
        )

        arguments = parser.parse_args()

        logging.basicConfig(level=getattr(logging, arguments.log_level.upper()))

        for key in vars(arguments):
            value = getattr(arguments, key)
            setattr(self, key, value)
            logger.info(f"argument {key}: {value}")

        self.execution_timestamp = datetime.now()
        self.execution_timestamp_str = self.execution_timestamp.strftime(
            '%Y-%m-%d %H:%M:%S'
        )
        self.used_arguments_str = used_arguments_str(arguments)
        self.version = __version__

        return self

    def parse_mapping_bundle_config(self):
        base_path = self.mapping_bundle_path
        config_path = os.path.join(base_path, 'tables.cfg')
        config_file = open(config_path)
        config = configparser.ConfigParser()
        config.read_file(config_file)
        for key, value in config['DEFAULT'].items():
            logger.info(f"config {key}: {value}")
        self.fragments_lookup_table_path = os.path.join(
            base_path,
            config['DEFAULT']['lookup_table']
        )
        self.fragments_type_table_path = os.path.join(
            base_path,
            config['DEFAULT']['other_annotations']
        )
        self.trna_sequences_path = os.path.join(
            base_path,
            config['DEFAULT']['trna_spliced_sequences']
        )
        self.assembly = config['DEFAULT']['assembly']
        self.mapping_bundle_version = config['DEFAULT']['version']

        config_file.close()
        return self

    def run(self):
        logger.debug(json.dumps(self.__dict__, default=lambda o: str(o)))
        Pipeline(self.config).run()
        return self
