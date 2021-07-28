from expects import *
from mamba import _it, context, describe, description, fit, it  # noqa: F401

from mintmap.annotations import Annotations

with describe(Annotations) as self:
    with description('.load_trna') as self:
        with it('imports a trna_fasta file'):
            path = "spec/support/tRNAspace.Spliced.Sequences.MINTmap_v1.fa"
            Annotations.load_trna_sequences(path)
            label = 'trna127_CysGCA_1_-_93981834_93981906'
            actual = Annotations.trna.find(label)
            expected = 'GGGGGTATAGCTCAGGTGGTAGAGCATTTGACTGCAGATCAAGAGGTCCCCG' \
                + 'GTTCAAATCCGGGTGCCCCCT'
            expect(actual).to(start_with(expected))

    with description('.load_fragments_type_table') as self:
        with it('imports fragment_type_annotations file'):
            path = "spec/support/OtherAnnotations.MINTmap_v1.txt"
            Annotations.load_fragments_type_table(path)
            actual = Annotations.fragment_type.find('AGATCAAGAGGTCCCCGG')
            expected = ['i-tRF']
            expect(actual).to(equal(expected))

    with description('.load_fragments_lookup_table') as self:
        with it('imports fragment_lookup_table'):
            path = "spec/support/LookupTable.tRFs.MINTmap_v1.txt"
            index = Annotations.load_fragments_lookup_table(path).index
            exclusive = [k for k, v in index.items() if v]
            ambiguous = [k for k, v in index.items() if not v]
            expect(len(exclusive)).to(equal(3))
            expect(len(ambiguous)).to(equal(1))
