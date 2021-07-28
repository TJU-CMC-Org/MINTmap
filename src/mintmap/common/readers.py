# readers.py

import gzip
import io
import itertools
import json
import logging
import os
import re
import shutil
import subprocess
import sys
from collections import defaultdict
from pprint import pprint  # noqa: F401

logger = logging.getLogger('readers')


def fastq(path):
    sequence_pattern = re.compile('^[ATCGN]+$')
    input_file = None
    path = str(path)

    if not os.path.exists(path):
        logger.critical(f"fastq: file {path} does not exist")
        sys.exit(1)

    if path.endswith('.gz') or path.endswith('.gzip'):
        logger.debug(f"{path} is compressed")
        if shutil.which("gunzip"):
            logger.debug('fastq: gunzip is in path')
            pipe = subprocess.Popen(
                ['gunzip',
                 '--stdout',
                 path],
                stdout=subprocess.PIPE
            )
            input_file = io.BytesIO(pipe.communicate()[0])
            if pipe.returncode != 0:
                raise Exception('error calling gunzip')
        else:
            logger.debug('fastq: gunzip is not in path')
            input_file = io.BufferedReader(gzip.open(path, 'rb'))
    else:
        logger.debug(f"fastq: {path} file is not compressed")
        input_file = open(path, 'rb')

    for num, line in enumerate(input_file, 1):
        if (((num - 2) % 4) == 0):
            line = line.decode(encoding='UTF-8', errors='strict').strip()
            if not sequence_pattern.match(line):
                msg = 'Unrecognized character in fastq sequence ' \
                    + f"at line {line}, only [ATCGN] characters are valid"
                raise Exception(msg)
            yield line
        else:
            continue
    input_file.close()


def fasta_with_labels(path):
    sequence_pattern = re.compile('^[ATCGN]+$')
    label_pattern = re.compile('^>.+$')
    input_file = None
    path = str(path)

    if path.endswith('.gz') or path.endswith('.gzip'):
        input_file = io.BufferedReader(gzip.open(path, 'rb'))
    else:
        input_file = open(path, 'rb')

    for line_1, line_2 in itertools.zip_longest(*[input_file] * 2):
        line_1 = line_1.decode(encoding='UTF-8', errors='strict').strip()
        line_2 = line_2.decode(encoding='UTF-8', errors='strict').strip()
        if not label_pattern.match(line_1):
            raise Exception(f'Invalid fasta label {line_1}')
        if not sequence_pattern.match(line_2):
            raise Exception(f'Invalid fasta sequence {line_2}')
        yield (line_1[1:], line_2)

    input_file.close()


def lookup_table(path):
    input_file = None
    path = str(path)

    if path.endswith('.gz') or path.endswith('.gzip'):
        input_file = io.BufferedReader(gzip.open(path, 'rb'))
    else:
        input_file = open(path, 'rb')

    for line in input_file:
        yield line.decode(encoding='UTF-8', errors='strict').strip()

    input_file.close()


def exit_if_fastq_file_is_not_trimmed(path):
    input_file = None
    path = str(path)
    histogram = defaultdict(lambda: 0)
    sequence_pattern = re.compile('^[ATCGN]+$')

    if not os.path.exists(path):
        logger.critical(f"file {path} does not exist")
        sys.exit(1)

    if path.endswith('.gz') or path.endswith('.gzip'):
        logger.debug(f"{path} is compressed")
        if shutil.which("gunzip"):
            logger.debug('gunzip is in path')
            pipe = subprocess.Popen(
                ['gunzip',
                 '--stdout',
                 path],
                stdout=subprocess.PIPE
            )
            input_file = io.BytesIO(pipe.communicate()[0])
            if pipe.returncode != 0:
                raise Exception('error calling gunzip')
        else:
            logger.debug('gunzip is not in path')
            input_file = io.BufferedReader(gzip.open(path, 'rb'))
    else:
        logger.debug(f"{path} file is not compressed")
        input_file = open(path, 'rb')

    for num, line in enumerate(input_file, 1):
        # check only the first 500 sequences
        if num > 2004:
            break

        if (((num - 2) % 4) == 0):
            line = line.decode(encoding='UTF-8', errors='strict').strip()
            if not sequence_pattern.match(line):
                msg = 'Unrecognized character in fastq sequence ' \
                    + f"at line {line}, only [ATCGN] characters are valid"
                raise Exception(msg)
            histogram[len(line)] += 1
        else:
            continue
    input_file.close()

    total_histogram_keys = len(histogram.keys())
    logger.debug(f"sequence length histogram: {json.dumps(histogram)}")
    logger.debug(f"total histogram keys: {total_histogram_keys}")

    if total_histogram_keys == 1:
        logger.critical(
            'The first 500 sequences in the input file have the same length '
            f"({list(histogram.keys())[0]}) "
            'which is an indication that the input file has not been trimmed. '
            'Please trim the adapters (e.g. using a tool such as cutadapt) and '
            'provide the trimmed input file.'
        )
        exit(1)
    else:
        logger.debug('file seems to be trimmed')
