# molecule.py

import re

from .fragment import Fragment


class Molecule():
    not_word_re = re.compile(r'\W')

    def __init__(self, opts={}):
        self.__dict__ = opts
        self.padded_sequence = self.not_word_re.sub('', self.padded_sequence)
        self.padded_sequence_length = len(self.padded_sequence)

        self.start = self.padding_size
        self.end = self.padded_sequence_length - self.padding_size
        self.sequence = self.padded_sequence[self.start:self.end]
        self.length = len(self.sequence)

        self.left_range = range(0, self.padding_size)
        self.right_range = range(
            self.padded_sequence_length - self.padding_size,
            self.padded_sequence_length
        )
        self.range = range(self.start, self.padding_size + self.length)

        if 'sense' in opts:
            if opts['sense'] == 'positive':
                self.strand = True
            elif opts['sense'] == 'negative':
                self.strand = False
            #else:
            #    msg = f"Molecule sense value is invalid: `{opts['sense']}`. " \
            #        + 'Valid values are: [positive, negative]'
            #    raise ValueError(msg)

    def __repr__(self):
        return f"<Molecule {self.__dict__}>"

    def region(self, region_id):
        return self.regions_index.get(region_id)

    @property
    def regions(self):
        return self.regions_index.values()

    def fragments(self, sequence):
        return [] \
            + self.__5utrf_fragments(sequence) \
            + self.__5trf_fragments(sequence) \
            + self.__itrf_fragments(sequence) \
            + self.__3trf_fragments(sequence) \
            + self.__trf_1s_fragments(sequence)

    def __5utrf_fragments(self, sequence):
        search_range = range(
            self.start - sequence.length + 1,
            self.start + sequence.length
        )

        start_positions = self.__substrings(
            substring=sequence.sequence,
            string=self.padded_sequence,
            search_range=search_range
        )

        return list(map(lambda start: Fragment(
            sequence=sequence,
            molecule=self,
            type='5-u-trf',
            start=start,  # zero indexed
            end=start + sequence.length - 1  # zero indexed, inclusive
        ), start_positions))

    def __5trf_fragments(self, sequence):
        search_range = range(self.start, self.start + sequence.length + 1)

        start_positions = list(
            self.__substrings(
                substring=sequence.sequence,
                string=self.padded_sequence,
                search_range=search_range
            )
        )

        search_range = range(self.start, self.start + sequence.length)
        start_positions.extend(
            self.__substrings(
                substring=sequence.sequence[1:],
                string=self.padded_sequence,
                search_range=search_range
            )
        )

        return list(map(lambda start: Fragment(
            sequence=sequence,
            molecule=self,
            type='5-trf',
            start=start - 1,  # zero indexed
            end=start - 1 + sequence.length - 1  # zero indexed, inclusive
        ), start_positions))

    def __itrf_fragments(self, sequence):
        search_range = range(self.start + 1, self.end + 1)

        start_positions = self.__substrings(
            substring=sequence.sequence,
            string=self.padded_sequence,
            search_range=search_range
        )

        return list(map(lambda start: Fragment(
            sequence=sequence,
            molecule=self,
            type='i-trf',
            start=start,  # zero indexed
            end=start + sequence.length - 1  # zero indexed, inclusive
        ), start_positions))

    def __3trf_fragments(self, sequence):
        search_range = range(self.end - sequence.length - 1, self.end + 5)
        start_positions = self.__substrings(
            substring=sequence.sequence,
            string=self.padded_sequence[:self.end] + 'CCA',
            search_range=search_range
        )

        filtered_start_positions = filter(
            lambda start: start + sequence.length > self.end,
            start_positions
        )

        return list(map(lambda start: Fragment(
            sequence=sequence,
            molecule=self,
            type='3-trf',
            start=start,  # zero indexed
            end=start + sequence.length - 1  # zero indexed, inclusive
        ), filtered_start_positions))

    def __trf_1s_fragments(self, sequence):
        search_range = range(
            self.end - sequence.length + 1,
            self.end + sequence.length
        )

        start_positions = self.__substrings(
            substring=sequence.sequence,
            string=self.padded_sequence,
            search_range=search_range
        )

        return list(map(lambda start: Fragment(
            sequence=sequence,
            molecule=self,
            type='trf-1s',
            start=start,  # zero indexed
            end=start + sequence.length - 1  # zero indexed, inclusive
        ), start_positions))

    def __substrings(self, substring, string, search_range):
        string = string[search_range[0]:search_range[-1]]
        offset = search_range[0]
        matches = re.finditer(rf"(?=({substring}))", string)
        return map(
            lambda position: position + offset,
            [match.start() for match in matches]
        )
