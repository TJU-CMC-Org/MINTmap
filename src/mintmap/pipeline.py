# pipeline.py

import logging
import time

from jinja2 import Environment, PackageLoader

from mintmap.annotations import Annotations
from mintmap.common import readers
from mintmap.sequence import Sequence

logger = logging.getLogger('pipeline')


class PipelineMetaClass(type):

    def _todo(self):
        return False


class Pipeline(metaclass=PipelineMetaClass):

    def __init__(self, config={}):
        for key, value in config.items():
            setattr(self, key, value)
        self.files = {
            'exclusive':
                {
                    'expression': {
                        'txt': None,
                        'html': None
                    },
                    'countsmeta': {
                        'txt': None
                    }
                },
            'ambiguous':
                {
                    'expression': {
                        'txt': None,
                        'html': None
                    },
                    'countsmeta': {
                        'txt': None
                    }
                }
        }

    def run(self):

        pipeline_start = time.time()
        Annotations.load_trna_sequences(self.trna_sequences_path)
        Annotations.load_fragments_type_table(self.fragments_type_table_path)
        Annotations.load_fragments_lookup_table(
            self.fragments_lookup_table_path
        )
        runtime = time.time() - pipeline_start
        logger.info(f"Annotation tables load in {round(runtime,2)} seconds")

        Sequence.custom_rpm = self.custom_rpm
        Sequence.assembly = self.assembly

        logger.info("Load fastq file")
        start = time.time()
        path = self.input_file_path

        readers.exit_if_fastq_file_is_not_trimmed(path)

        for seq in readers.fastq(path):
            Sequence.add(seq)

        runtime = time.time() - start
        logger.info(f"Fastq file processed in {round(runtime,2)} seconds")

        logger.info("Write output files")
        start = time.time()
        self.write_output_files()
        runtime = time.time() - start
        logger.info(f"Output files written in {round(runtime,2)} seconds")

        runtime = time.time() - pipeline_start
        logger.info(f"Pipeline run in {round(runtime,2)} seconds")
        return self

    def write_output_files(self):
        all_reads_count = Sequence.all_reads_count
        templates = Environment(
            loader=PackageLoader('mintmap',
                                 'templates'),
            autoescape=False
        )

        # open files
        for fragment_type in self.files.keys():
            for content_type in self.files[fragment_type].keys():
                for file_type in self.files[fragment_type][content_type].keys():
                    filename = self.prefix \
                        + f'-MINTmap_{self.version}-{fragment_type}-' \
                        + f'tRFs.{content_type}.{file_type}'
                    self.files[fragment_type][content_type][file_type] = open(
                        filename,
                        'w+'
                    )

        # write file headers
        for fragment_type in self.files.keys():
            reads_count = getattr(
                Sequence,
                f"{fragment_type}_fragments_reads_count"
            )

            template_args = {
                **self.__dict__,
                **{
                    'fragment_type': fragment_type,
                    'reads_count': reads_count,
                    'all_reads_count': all_reads_count,
                }
            }

            template = templates.get_template('output_header.txt.j2')
            self.files[fragment_type]['expression']['txt'] \
                .write(template.render(**template_args))

            template = templates.get_template('output_header.html.j2')
            self.files[fragment_type]['expression']['html'] \
                .write(template.render(**template_args))

        # write expression files
        for sequence in Sequence.all_fragments:
            f_type = 'exclusive' if sequence.is_exclusive else 'ambiguous'
            self.files[f_type]['expression']['txt'].write(
                sequence.to_txt + "\n"
            )
            self.files[f_type]['expression']['html'].write(
                f"      {sequence.to_html}\n"
            )

        # write countsmeta files
        for fragment_type in ['exclusive', 'ambiguous']:
            reads_count = getattr(
                Sequence,
                f"{fragment_type}_fragments_reads_count"
            )

            percentage = round(reads_count / all_reads_count * 100, 2)

            template_args = {
                **self.__dict__,
                **{
                    'fragment_type': fragment_type,
                    'reads_count': reads_count,
                    'all_reads_count': all_reads_count,
                    'percentage': percentage,
                }
            }

            template = templates.get_template('countsmeta.txt.j2')
            self.files[fragment_type]['countsmeta']['txt'] \
                .write(template.render(**template_args))

        # write file footers
        for fragment_type in self.files.keys():
            template = templates.get_template('output_footer.html.j2')
            self.files[fragment_type]['expression']['html'].write(
                template.render()
            )

        #close files
        for fragment_type in self.files.keys():
            for content_type in self.files[fragment_type].keys():
                for file_type in self.files[fragment_type][content_type].keys():
                    self.files[fragment_type][content_type][file_type].close()
