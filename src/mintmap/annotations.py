# annotations.py

import logging
import re

import yaml

from mintmap.common.helpers import open_file, slice

logger = logging.getLogger('annotations')


class AnnotationsMetaClass(type):

    @property
    def to_yaml(self):
        obj = {}
        if self.trna:
            obj["trna"] = self.trna.index
        return yaml.dump(obj, allow_unicode=True, default_flow_style=False)


class Annotations(metaclass=AnnotationsMetaClass):
    trna = None
    fragment_type = None
    fragment_exclusivity = None

    @classmethod
    def load_fragments_type_table(self, path):
        logger.debug(f"load_fragments_type_table {path}")
        index = {}
        lines = open_file(path)
        for line in lines:
            tokens = line.strip().replace(',', '').split()
            index[tokens[0]] = tokens[1:]
        #index = dict(splitted)
        self.fragment_type = Annotations(index)
        return self.fragment_type

    @classmethod
    def load_trna_sequences(self, path):
        logger.debug(f"load_trna_sequences {path}")
        index = {}
        fasta_label_pattern = re.compile('^>[-.|+_A-Za-z0-9]+$')
        fasta_value_pattern = re.compile('^[ATCGN]+$')
        slices = slice(open_file(path), 2)

        for i in slices:
            key = i[0]
            value = i[1]

            if not fasta_label_pattern.match(key):
                msg = 'Only characters [>-.|+_A-Za-z0-9] allowed in ' \
                    + f'FASTA label but received {key}'
                raise Exception(msg)

            if not fasta_value_pattern.match(value):
                msg = 'Only characters [ATCGN] allowed in ' \
                    + f'FASTA sequence but received {value}'
                raise Exception(msg)

            key = key.replace('>', '')
            index[key] = value
        self.trna = Annotations(index)
        return self.trna

    @classmethod
    def load_fragments_lookup_table(self, path):
        logger.debug(f"load_fragments_lookup_table {path}")
        index = {}

        lines = open_file(path)
        lines_uncommented = filter(lambda line: not line.startswith('#'), lines)
        splitted = map(lambda i: i.split("\t")[0:2], lines_uncommented)

        # Note: a Y in col2 means the tRF sequence is exclusive to tRNA space
        # and a N means it's not exclusive

        for a in splitted:
            if a[1] == 'Y':
                index[a[0]] = True
            elif a[1] == 'N':
                index[a[0]] = False

        self.fragment_exclusivity = Annotations(index)
        return self.fragment_exclusivity

    def __init__(self, index):
        self.index = index

    def __str__(self):
        return self.to_yaml

    def filter(self, func):
        return [k for k, v in self.index.items() if func(k, v)]

    def find(self, label):
        return self.index[label]

    def get(self, label):
        return self.index.get(label)

    def has_key(self, key):
        return self.index.__contains__(key)

    @property
    def to_yaml(self):
        obj = self.index
        return yaml.dump(obj, allow_unicode=True, default_flow_style=False)
