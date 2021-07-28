# sequence.py

import functools
import re

import mintmap.common.mintplates as mintplates
from mintmap.annotations import Annotations


class SequenceMetaClass(type):

    @property
    def all_fragments(self):
        '''Sorted list of sequences'''

        return sorted(
            self.all_fragments_index.values(),
            key=functools.cmp_to_key(self._comp_sequences),
            reverse=True
        )


class Sequence(metaclass=SequenceMetaClass):
    __slots__ = ['is_exclusive', 'is_fragment', 'sequence', 'reads_count']

    all_reads_count = 0
    all_fragments_index = {}
    all_fragments_reads_count = 0
    ambiguous_fragments_reads_count = 0
    assembly = None
    custom_rpm = None
    exclusive_fragments_reads_count = 0
    fragments_reads_count = 0

    @classmethod
    def add(self, sequence):
        '''Add a Sequence. Increases the all_reads_count counter. If the
        sequence is a fragment, add it to the index and increase related
        counters'''

        s = self.get_or_create(sequence)
        s.is_exclusive = Annotations.fragment_exclusivity.get(sequence)
        s.is_fragment = False if s.is_exclusive is None else True
        s.reads_count += 1
        self.all_reads_count += 1

        if s.is_fragment:
            self.all_fragments_reads_count += 1
            self.all_fragments_index[sequence] = s
            if s.is_exclusive:
                self.exclusive_fragments_reads_count += 1
            else:
                self.ambiguous_fragments_reads_count += 1

        return s

    @classmethod
    def _comp_sequences(self, a, b):
        '''Sequences compare function. Compares by reads_count and then
        by sequence string'''

        if a.reads_count > b.reads_count:
            return 1
        elif a.reads_count < b.reads_count:
            return -1
        elif a.sequence > b.sequence:
            return -1
        elif a.sequence < b.sequence:
            return 1

    @classmethod
    def get(self, sequence):
        return self.all_fragments_index.get(sequence)

    @classmethod
    def get_or_create(self, sequence):
        s = self.get(sequence)
        if s is not None:
            return s
        else:
            return Sequence(sequence)

    @classmethod
    def reset(self):
        '''Reset class variables to default values. This is used in tests'''

        Sequence.all_reads_count = 0
        Sequence.all_fragments_index = {}
        Sequence.all_fragments_reads_count = 0
        Sequence.ambiguous_fragments_reads_count = 0
        Sequence.assembly = None
        Sequence.custom_rpm = None
        Sequence.exclusive_fragments_reads_count = 0
        Sequence.fragments_reads_count = 0

    def __init__(self, sequence):
        self.sequence = sequence
        self.reads_count = 0  # Sequence.add() increases the counter

    def __str__(self):
        return ' '.join(
            [
                '<Sequence',
                str(self.sequence),
                str(self.reads_count),
                f"{self.is_fragment}>"
            ]
        )

    @property
    def annotations(self):
        '''Annotations across all tRNA spliced sequences.
        Returns a list of strings'''

        annotations = []
        for trna_name in Annotations.trna.index:
            for annotation in self.annotations_of_a_trna(trna_name):
                annotations.append(annotation)
        annotations.sort()
        return annotations

    def annotations_of_a_trna(self, trna_name):
        padding_size = 49

        annotations = []
        trna_padded_sequence = Annotations.trna.find(trna_name)

        # 5-trf
        trunc = False
        partial_start = padding_size
        partial_end = padding_size + self.length - 1
        trna_partial_sequence = trna_padded_sequence[partial_start:partial_end]
        self_partial_sequence = self.sequence[1:]
        if trna_partial_sequence == self_partial_sequence:
            trunc = True
            annotation = f"{trna_name}@" \
                + f"{-1}{self.sequence[0:1] if trunc else ''}." \
                + f"{self.length - 1}." \
                + f"{self.length}"
            annotations.append(annotation)
            #print("\nmatch 5-trf a")
            #print(trna_name)
            #print(trna_partial_sequence)
            #print(annotation)

        # 5-u-trf
        partial_start = padding_size - self.length + 1
        partial_end = padding_size + self.length - 1
        trna_partial_sequence = trna_padded_sequence[partial_start:partial_end]
        matches = re.finditer(self.sequence, trna_partial_sequence)
        matches_positions = [match.start() for match in matches]

        for position in matches_positions:
            annotation = f"{trna_name}@" \
                + f"{position - self.length + 1}" \
                + f"{self.sequence[0:1] if trunc else ''}." \
                + f"{position + 1}." \
                + f"{self.length}"
            annotations.append(annotation)
            #print("\nmatch 5-u-trf")
            #print(trna_name)
            #print(self.sequence)
            #print(trna_partial_sequence)
            #print(position)
            #print(annotation)

        # 5-trf
        partial_start = padding_size
        partial_end = padding_size + self.length
        trna_partial_sequence = trna_padded_sequence[partial_start:partial_end]
        if trna_partial_sequence == self.sequence:
            annotation = f"{trna_name}@" \
                + f"{1}." \
                + f"{self.length}." \
                + f"{self.length}"
            annotations.append(annotation)
            #print("\nmatch 5-trf b")
            #print(trna_name)
            #print(trna_partial_sequence)
            #print(annotation)

        # i-trf
        partial_start = padding_size + 1
        partial_end = len(trna_padded_sequence) - padding_size
        trna_partial_sequence = trna_padded_sequence[partial_start:partial_end]
        matches = re.finditer(self.sequence, trna_partial_sequence)
        matches_positions = [match.start() for match in matches]
        for position in matches_positions:
            annotation = f"{trna_name}@" \
                + f"{position + 2}." \
                + f"{position + 1 + self.length}." \
                + f"{self.length}"
            annotations.append(annotation)
            #print("\nmatch i-trf")
            #print(trna_name)
            #print(position)
            #print(self.sequence)
            #print(trna_partial_sequence)
            #print(annotation)
        # 3-trf
        partial_start = len(
            trna_padded_sequence
        ) - padding_size - self.length + 1
        partial_end = len(trna_padded_sequence) - padding_size
        trna_partial_sequence = trna_padded_sequence[partial_start:partial_end]\
            + "CCA"
        matches = re.finditer(self.sequence, trna_partial_sequence)
        matches_positions = [match.start() for match in matches]
        for position in matches_positions:
            annotation = f"{trna_name}@" \
                + f"{position + partial_start - padding_size + 1}." \
                + f"{position + partial_start - padding_size + self.length}." \
                + f"{self.length}"
            annotations.append(annotation)
            #print("\nmatch 3-trf")
            #print(trna_name)
            #print(position)
            #print(self.sequence)
            #print(trna_partial_sequence)
            #print(annotation)

        # 1s-trf
        partial_start = len(
            trna_padded_sequence
        ) - padding_size - self.length + 1
        partial_end = len(trna_padded_sequence) - padding_size + self.length - 1
        trna_partial_sequence = trna_padded_sequence[partial_start:partial_end]
        matches = re.finditer(self.sequence, trna_partial_sequence)
        matches_positions = [match.start() for match in matches]
        for position in matches_positions:
            annotation = f"{trna_name}@" \
                + f"{position + partial_start - padding_size + 1}." \
                + f"{position + partial_start - padding_size + self.length}." \
                + f"{self.length}"
            annotations.append(annotation)
            #print("\nmatch 1s-trf")
            #print(trna_name)
            #print(position)
            #print(self.sequence)
            #print(trna_partial_sequence)
            #print(annotation)

        annotations.sort()
        return annotations
        trna_sequence = Annotations.trna.find(trna_name) + 'CCA'
        trf5ptrunc = self.sequence[1:]

        if trna_sequence.startswith(trf5ptrunc):
            annotation = f"{trna_name}@-1{self.sequence[:1]}." \
                + f"{len(trf5ptrunc)}.{self.length}"
            annotations.append(annotation)

        matches = re.finditer(self.sequence, trna_sequence)
        matches_positions = [match.start() for match in matches]

        for position in matches_positions:
            annotation = f"{trna_name}@"\
                + f"{position + 1}.{position + self.length}.{self.length}"
            annotations.append(annotation)

        annotations.sort()
        return annotations

    @property
    def exclusivity_group_reads_count(self):
        if self.is_exclusive:
            return Sequence.exclusive_fragments_reads_count
        else:
            return Sequence.ambiguous_fragments_reads_count

    @property
    def length(self):
        return len(self.sequence)

    @property
    def licence_plate(self):
        return mintplates.convert(self.sequence, True, 'tRF')

    @property
    def rpm_1(self):
        rpm = (
            self.reads_count / self.exclusivity_group_reads_count
        ) * 1_000_000
        return "{:.2f}".format(rpm)

    @property
    def rpm_2(self):
        rpm = (self.reads_count / Sequence.all_reads_count) * 1_000_000
        return "{:.2f}".format(rpm)

    @property
    def rpm_3(self):
        if Sequence.custom_rpm:
            rpm = (self.reads_count / Sequence.custom_rpm) * 1_000_000
            return "{:.2f}".format(rpm)
        else:
            return 'na'

    @property
    def to_txt(self):
        output_items = [
            self.licence_plate,
            self.sequence,
            ", ".join(self.fragment_type),
            self.reads_count,
            self.rpm_1,
            self.rpm_2,
            self.rpm_3,
            ", ".join(self.annotations)
        ]
        return "\t".join(map(lambda i: str(i), output_items))

    @property
    def fragment_type(self):
        '''get fragment type from other annotations'''

        return Annotations.fragment_type.get(self.sequence)

    @property
    def to_html(self):
        output_items = [
            self.licence_plate,
            self.sequence,
            ", ".join(self.fragment_type),
            self.reads_count,
            self.rpm_1,
            self.rpm_2,
            self.rpm_3,
            f"""<a target='_blank' href='{self.url}'>Summary</a>""",
            ", ".join(self.annotations)
        ]
        tds = "".join(map(lambda i: f'<td>{str(i)}</td>', output_items))
        tr = f'<tr>{tds}</tr>'
        return tr

    @property
    def url(self):
        return "https://cm.jefferson.edu/MINTbase/InputController" \
            + f"?g={Sequence.assembly}&v=s&fs={self.sequence}"
