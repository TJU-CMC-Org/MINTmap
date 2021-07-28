# sequence.py

import functools

import mintmap.common.mintplates as mintplates


class SequenceMetaClass(type):

    @property
    def all(self):
        '''Sorted list of expressed sequences'''
        filtered = filter(lambda s: s.reads_count > 0, self.index.values())
        return sorted(
            filtered,
            key=functools.cmp_to_key(self._comp_sequences),
            reverse=True
        )


class Sequence(metaclass=SequenceMetaClass):
    __slots__ = ['sequence', 'reads_count']

    all_reads_count = 0
    assembly = None
    custom_rpm = None
    index = {}
    indexed_reads_count = 0

    def __init__(self, sequence):
        self.sequence = sequence
        self.reads_count = 0  # Sequence.add() increases the counter

    def __repr__(self):
        seq = self.sequence
        if self.length > 50:
            seq = seq[:50 - 3] + '...'
        return f"<Sequence {seq} {self.length} {self.reads_count}>"

    @classmethod
    def _comp_sequences(self, a, b):
        return a.compare_to_sequence(b)

    def compare_to_sequence(self, other):
        if self.reads_count > other.reads_count:
            return 1
        elif self.reads_count < other.reads_count:
            return -1
        elif self.sequence > other.sequence:
            return -1
        elif self.sequence < other.sequence:
            return 1

    @classmethod
    def add_to_index(self, sequence):
        if sequence.sequence not in self.index:
            self.index[sequence.sequence] = sequence

    @classmethod
    def increase_reads_count(self, sequence_str):
        self.all_reads_count += 1
        if sequence_str in self.index:
            self.index[sequence_str].reads_count += 1
            self.indexed_reads_count += 1

    @classmethod
    def get(self, sequence_str):
        return self.index.get(sequence_str)

    @property
    def length(self):
        return len(self.sequence)

    @property
    def licence_plate(self):
        return mintplates.convert(self.sequence, True, self.tag)

    @property
    def reverse_complement(self):
        intab = "ATCG"
        outtab = "TAGC"
        translation = self.sequence.maketrans(intab, outtab)
        complement = self.sequence.translate(translation)
        reverse_complement = complement[::-1]
        return reverse_complement
