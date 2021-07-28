import random

from expects import *
from mamba import _it, context, describe, description, fit, it  # noqa: F401

from mintmap.annotations import Annotations
from mintmap.sequence import Sequence

# types and annotations of trnaMT_SerGCT_MT_+_12207_12265@-15.1.16
#
# cat src/mintmap/mappingbundle/v2/tRNAspace.Spliced.Sequences.With49ntFlank.MINTmap_v2.fa \ # noqa: E501
# | grep -A 1 trnaMT_SerGCT_MT_+_12207_12265 \
# > spec/support/tRNAspace.Spliced.Sequences.MINTmap_v2.fa
#
# ACATCAGATTGTGAAT 0 []
# CATCAGATTGTGAATC 1 []
# ATCAGATTGTGAATCT 2 []
# TCAGATTGTGAATCTG 3 []
# CAGATTGTGAATCTGA 4 []
# AGATTGTGAATCTGAC 5 []
# GATTGTGAATCTGACA 6 []
# ATTGTGAATCTGACAA 7 []
# TTGTGAATCTGACAAC 8 []
# TGTGAATCTGACAACA 9 []
# GTGAATCTGACAACAG 10 []
# TGAATCTGACAACAGA 11 []
# GAATCTGACAACAGAG 12 []
# AATCTGACAACAGAGG 13 []
# ATCTGACAACAGAGGC 14 []
# TCTGACAACAGAGGCT 15 []
# CTGACAACAGAGGCTT 16 []
# TGACAACAGAGGCTTA 17 []
# GACAACAGAGGCTTAC 18 []
# ACAACAGAGGCTTACG 19 []
# CAACAGAGGCTTACGA 20 []
# AACAGAGGCTTACGAC 21 []
# ACAGAGGCTTACGACC 22 []
# CAGAGGCTTACGACCC 23 []
# AGAGGCTTACGACCCC 24 []
# GAGGCTTACGACCCCT 25 []
# AGGCTTACGACCCCTT 26 []
# GGCTTACGACCCCTTA 27 []
# GCTTACGACCCCTTAT 28 []
# CTTACGACCCCTTATT 29 []
# TTACGACCCCTTATTT 30 []
# TACGACCCCTTATTTA 31 []
# ACGACCCCTTATTTAC 32 []
# CGACCCCTTATTTACC 33 []
# GACCCCTTATTTACCG 34 ['5-u-trf'] trnaMT_SerGCT_MT_+_12207_12265@-15.1.16
# ACCCCTTATTTACCGA 35 ['5-u-trf']
# CCCCTTATTTACCGAG 36 ['5-u-trf']
# CCCTTATTTACCGAGA 37 ['5-u-trf']
# CCTTATTTACCGAGAA 38 ['5-u-trf']
# CTTATTTACCGAGAAA 39 ['5-u-trf']
# TTATTTACCGAGAAAG 40 ['5-u-trf']
# TATTTACCGAGAAAGC 41 ['5-u-trf']
# ATTTACCGAGAAAGCT 42 ['5-u-trf']
# TTTACCGAGAAAGCTC 43 ['5-u-trf']
# TTACCGAGAAAGCTCA 44 ['5-u-trf']
# TACCGAGAAAGCTCAC 45 ['5-u-trf']
# ACCGAGAAAGCTCACA 46 ['5-u-trf']
# CCGAGAAAGCTCACAA 47 ['5-u-trf'] trnaMT_SerGCT_MT_+_12207_12265@-2.14.16
# CGAGAAAGCTCACAAG 48 ['5-u-trf', '5-trf'] trnaMT_SerGCT_MT_+_12207_12265@-1C.15.16 trnaMT_SerGCT_MT_+_12207_12265@-1C.15.16 # noqa: E501
# AGAGAAAGCTCACAAG 48 ['5-trf'] extra trnaMT_SerGCT_MT_+_12207_12265@-1A.15.16
# TGAGAAAGCTCACAAG 48 ['5-trf'] extra trnaMT_SerGCT_MT_+_12207_12265@-1T.15.16
# GGAGAAAGCTCACAAG 48 ['5-trf'] extra trnaMT_SerGCT_MT_+_12207_12265@-1G.15.16
# GAGAAAGCTCACAAGA 49 ['5-trf'] trnaMT_SerGCT_MT_+_12207_12265@1.16.16
# AGAAAGCTCACAAGAA 50 ['i-trf'] trnaMT_SerGCT_MT_+_12207_12265@2.17.16
# GAAAGCTCACAAGAAC 51 ['i-trf']
# AAAGCTCACAAGAACT 52 ['i-trf']
# AAGCTCACAAGAACTG 53 ['i-trf']
# AGCTCACAAGAACTGC 54 ['i-trf']
# GCTCACAAGAACTGCT 55 ['i-trf']
# CTCACAAGAACTGCTA 56 ['i-trf']
# TCACAAGAACTGCTAA 57 ['i-trf']
# CACAAGAACTGCTAAC 58 ['i-trf']
# ACAAGAACTGCTAACT 59 ['i-trf']
# CAAGAACTGCTAACTC 60 ['i-trf']
# AAGAACTGCTAACTCA 61 ['i-trf']
# AGAACTGCTAACTCAT 62 ['i-trf']
# GAACTGCTAACTCATG 63 ['i-trf']
# AACTGCTAACTCATGC 64 ['i-trf']
# ACTGCTAACTCATGCC 65 ['i-trf']
# CTGCTAACTCATGCCC 66 ['i-trf']
# TGCTAACTCATGCCCC 67 ['i-trf']
# GCTAACTCATGCCCCC 68 ['i-trf']
# CTAACTCATGCCCCCA 69 ['i-trf']
# TAACTCATGCCCCCAT 70 ['i-trf']
# AACTCATGCCCCCATG 71 ['i-trf']
# ACTCATGCCCCCATGT 72 ['i-trf']
# CTCATGCCCCCATGTC 73 ['i-trf']
# TCATGCCCCCATGTCT 74 ['i-trf']
# CATGCCCCCATGTCTA 75 ['i-trf']
# ATGCCCCCATGTCTAA 76 ['i-trf']
# TGCCCCCATGTCTAAC 77 ['i-trf']
# GCCCCCATGTCTAACA 78 ['i-trf']
# CCCCCATGTCTAACAA 79 ['i-trf']
# CCCCATGTCTAACAAC 80 ['i-trf']
# CCCATGTCTAACAACA 81 ['i-trf']
# CCATGTCTAACAACAT 82 ['i-trf']
# CATGTCTAACAACATG 83 ['i-trf']
# ATGTCTAACAACATGG 84 ['i-trf']
# TGTCTAACAACATGGC 85 ['i-trf']
# GTCTAACAACATGGCT 86 ['i-trf']
# TCTAACAACATGGCTT 87 ['i-trf']
# CTAACAACATGGCTTT 88 ['i-trf']
# TAACAACATGGCTTTC 89 ['i-trf']
# AACAACATGGCTTTCT 90 ['i-trf']
# ACAACATGGCTTTCTC 91 ['i-trf']
# CAACATGGCTTTCTCA 92 ['i-trf'] trnaMT_SerGCT_MT_+_12207_12265@44.59.16
# AACATGGCTTTCTCAC 93 ['3-trf'] extra trnaMT_SerGCT_MT_+_12207_12265@45.60.16
# ACATGGCTTTCTCACC 94 ['3-trf'] extra trnaMT_SerGCT_MT_+_12207_12265@46.61.16
# CATGGCTTTCTCACCA 95 ['3-trf'] extra trnaMT_SerGCT_MT_+_12207_12265@47.62.16
# AACATGGCTTTCTCAA 93 ['trf-1s'] trnaMT_SerGCT_MT_+_12207_12265@45.60.16
# ACATGGCTTTCTCAAC 94 ['trf-1s']
# CATGGCTTTCTCAACT 95 ['trf-1s']
# ATGGCTTTCTCAACTT 96 ['trf-1s']
# TGGCTTTCTCAACTTT 97 ['trf-1s']
# GGCTTTCTCAACTTTT 98 ['trf-1s']
# GCTTTCTCAACTTTTA 99 ['trf-1s']
# CTTTCTCAACTTTTAA 100 ['trf-1s']
# TTTCTCAACTTTTAAA 101 ['trf-1s']
# TTCTCAACTTTTAAAG 102 ['trf-1s']
# TCTCAACTTTTAAAGG 103 ['trf-1s']
# CTCAACTTTTAAAGGA 104 ['trf-1s']
# TCAACTTTTAAAGGAT 105 ['trf-1s']
# CAACTTTTAAAGGATA 106 ['trf-1s']
# AACTTTTAAAGGATAA 107 ['trf-1s'] trnaMT_SerGCT_MT_+_12207_12265@59.74.16
# ACTTTTAAAGGATAAC 108 []
# CTTTTAAAGGATAACA 109 []
# TTTTAAAGGATAACAG 110 []
# TTTAAAGGATAACAGC 111 []
# TTAAAGGATAACAGCT 112 []
# TAAAGGATAACAGCTA 113 []
# AAAGGATAACAGCTAT 114 []
# AAGGATAACAGCTATC 115 []
# AGGATAACAGCTATCC 116 []
# GGATAACAGCTATCCA 117 []
# GATAACAGCTATCCAT 118 []
# ATAACAGCTATCCATT 119 []
# TAACAGCTATCCATTG 120 []
# AACAGCTATCCATTGG 121 []
# ACAGCTATCCATTGGT 122 []
# CAGCTATCCATTGGTC 123 []
# AGCTATCCATTGGTCT 124 []
# GCTATCCATTGGTCTT 125 []
# CTATCCATTGGTCTTA 126 []
# TATCCATTGGTCTTAG 127 []
# ATCCATTGGTCTTAGG 128 []
# TCCATTGGTCTTAGGC 129 []
# CCATTGGTCTTAGGCC 130 []
# CATTGGTCTTAGGCCC 131 []
# ATTGGTCTTAGGCCCC 132 []
# TTGGTCTTAGGCCCCA 133 []
# TGGTCTTAGGCCCCAA 134 []
# GGTCTTAGGCCCCAAA 135 []
# GTCTTAGGCCCCAAAA 136 []
# TCTTAGGCCCCAAAAA 137 []
# CTTAGGCCCCAAAAAT 138 []
# TTAGGCCCCAAAAATT 139 []
# TAGGCCCCAAAAATTT 140 []
# AGGCCCCAAAAATTTT 141 []

# yapf:disable
expectations = [
    # GACCCCTTATTTACCG 34 ['5-u-trf'] trnaMT_SerGCT_MT_+_12207_12265@-15.1.16
    {
        "sequence": "GACCCCTTATTTACCG",
        "annotations": ["trnaMT_SerGCT_MT_+_12207_12265@-15.1.16"],
        "types": ['5-u-trf']
    },
    # CCGAGAAAGCTCACAA 47 ['5-u-trf'] trnaMT_SerGCT_MT_+_12207_12265@-2.14.16
    {
        "sequence": "CCGAGAAAGCTCACAA",
        "types": ['5-u-trf'],
        "annotations": ["trnaMT_SerGCT_MT_+_12207_12265@-2.14.16"]
    },
    # CGAGAAAGCTCACAAG 48 ['5-u-trf', '5-trf'] trnaMT_SerGCT_MT_+_12207_12265@-1C.15.16 trnaMT_SerGCT_MT_+_12207_12265@-1C.15.16 # noqa: E501
    {
        "sequence": "CGAGAAAGCTCACAAG",
        "types": ['5-u-trf', '5-trf'],
        "annotations": [
            "trnaMT_SerGCT_MT_+_12207_12265@-1C.15.16",
            "trnaMT_SerGCT_MT_+_12207_12265@-1C.15.16"
        ]
    },
    # AGAGAAAGCTCACAAG 48 ['5-trf'] extra trnaMT_SerGCT_MT_+_12207_12265@-1A.15.16 # noqa: E501
    {
        "sequence": "AGAGAAAGCTCACAAG",
        "types": ['5-trf'],
        "annotations": ["trnaMT_SerGCT_MT_+_12207_12265@-1A.15.16"]
    },
    # TGAGAAAGCTCACAAG 48 ['5-trf'] extra trnaMT_SerGCT_MT_+_12207_12265@-1T.15.16 # noqa: E501
    {
        "sequence": "TGAGAAAGCTCACAAG",
        "types": ['5-trf'],
        "annotations": ["trnaMT_SerGCT_MT_+_12207_12265@-1T.15.16"]
    },
    # GGAGAAAGCTCACAAG 48 ['5-trf'] extra trnaMT_SerGCT_MT_+_12207_12265@-1G.15.16 # noqa: E501
    {
        "sequence": "GGAGAAAGCTCACAAG",
        "types": ['5-trf'],
        "annotations": ["trnaMT_SerGCT_MT_+_12207_12265@-1G.15.16"]
    },
    # GAGAAAGCTCACAAGA 49 ['5-trf'] trnaMT_SerGCT_MT_+_12207_12265@1.16.16
    {
        "sequence": "GAGAAAGCTCACAAGA",
        "types": ['5-trf'],
        "annotations": ["trnaMT_SerGCT_MT_+_12207_12265@1.16.16"]
    },
    # AGAAAGCTCACAAGAA 50 ['i-trf'] trnaMT_SerGCT_MT_+_12207_12265@2.17.16
    {
        "sequence": "AGAAAGCTCACAAGAA",
        "types": ['i-trf'],
        "annotations": ["trnaMT_SerGCT_MT_+_12207_12265@2.17.16"]
    },
    # CAACATGGCTTTCTCA 92 ['i-trf'] trnaMT_SerGCT_MT_+_12207_12265@44.59.16
    {
        "sequence": "CAACATGGCTTTCTCA",
        "types": ['i-trf'],
        "annotations": ["trnaMT_SerGCT_MT_+_12207_12265@44.59.16"]
    },
    # AACATGGCTTTCTCAC 93 ['3-trf'] extra trnaMT_SerGCT_MT_+_12207_12265@45.60.16 # noqa: E501
    {
        "sequence": "AACATGGCTTTCTCAC",
        "types": ['3-trf'],
        "annotations": ["trnaMT_SerGCT_MT_+_12207_12265@45.60.16"]
    },
    # ACATGGCTTTCTCACC 94 ['3-trf'] extra trnaMT_SerGCT_MT_+_12207_12265@46.61.16 # noqa: E501
    {
        "sequence": "ACATGGCTTTCTCACC",
        "types": ['3-trf'],
        "annotations": ["trnaMT_SerGCT_MT_+_12207_12265@46.61.16"]
    },
    # CATGGCTTTCTCACCA 95 ['3-trf'] extra trnaMT_SerGCT_MT_+_12207_12265@47.62.16 # noqa: E501
    {
        "sequence": "CATGGCTTTCTCACCA",
        "types": ['3-trf'],
        "annotations": ["trnaMT_SerGCT_MT_+_12207_12265@47.62.16"]
    },
    # AACATGGCTTTCTCAA 93 ['trf-1s'] trnaMT_SerGCT_MT_+_12207_12265@45.60.16
    {
        "sequence": "AACATGGCTTTCTCAA",
        "types": ['trf-1s'],
        "annotations": ["trnaMT_SerGCT_MT_+_12207_12265@45.60.16"]
    },
    # AACTTTTAAAGGATAA 107 ['trf-1s'] trnaMT_SerGCT_MT_+_12207_12265@59.74.16
    {
        "sequence": "AACTTTTAAAGGATAA",
        "types": ['trf-1s'],
        "annotations": ["trnaMT_SerGCT_MT_+_12207_12265@59.74.16"]
    },
]
# yapf:enable

with describe(Sequence) as self:
    with before.all:
        path = 'spec/support/tRNAspace.Spliced.Sequences.MINTmap_v2.fa'
        Annotations.load_trna_sequences(path)

    with description('Sequence()'):
        with it('creates a Sequence object'):
            Sequence('GGTAAATATAGTTTAAC')  # doesn't throw an exception

    with description('#annotations_of_a_trna'):
        with context('when trna is trnaMT_SerGCT_MT_+_12207_12265'):
            with it("sequences match expectations"):
                for e in expectations:
                    s = Sequence(e['sequence'])
                    trna_name = 'trnaMT_SerGCT_MT_+_12207_12265'
                    actual = s.annotations_of_a_trna(trna_name)
                    expected = e['annotations']
                    expect(actual).to(equal(expected))

    with description('#annotations'):
        with it('returns a populated array with annotation strings'):
            s = Sequence(expectations[0]['sequence'])
            actual = s.annotations
            expected = expectations[0]['annotations']
            expect(actual).to(contain(*expected))

    with description('.all_fragments'):
        with context('when all sequeces have the same reads_count'):
            with it('returns sequences ordered by sequence'):
                Sequence.reset()
                expected = ['AA', 'AT', 'CA', 'CT', 'GA', 'GT', 'TA', 'TG']
                shuffled = expected[:]
                random.shuffle(shuffled)
                for s in shuffled:
                    Sequence.all_fragments_index[s] = Sequence(s)
                actual = list(map(lambda i: i.sequence, Sequence.all_fragments))
                expect(actual).to(equal(expected))

        with context('when all sequeces have random reads_count'):
            with it('returns sequences ordered by reads_count'):
                Sequence.reset()
                sequences = ['AA', 'AT', 'CA', 'CT', 'GA', 'GT', 'TA', 'TG']
                random.shuffle(sequences)
                reads_counts = []
                for s in sequences:
                    Sequence.all_fragments_index[s] = Sequence(s)
                    Sequence.all_fragments_index[
                        s].reads_count = random.randint(1,
                                                        1000)
                actual = list(
                    map(lambda i: i.reads_count,
                        Sequence.all_fragments)
                )
                expected = sorted(actual, reverse=True)
                expect(actual).to(equal(expected))
