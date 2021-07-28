import types

from expects import *
from mamba import _it, context, describe, description, fit, it  # noqa: F401

from mintmap.common.readers import *

with description('common') as self:
    with description('readers') as self:
        with it('.read_fasta_with_labels') as self:
            fa = fasta_with_labels(
                'spec/support/tRNAspace.Spliced.Sequences.MINTmap_v1.fa'
            )
            expect(next(fa)[0]) \
                .to(equal('trna127_CysGCA_1_-_93981834_93981906'))

        with it('.lookup_table') as self:
            l = lookup_table('spec/support/LookupTable.tRFs.MINTmap_v1.txt')
            expect(l).to(be_a(types.GeneratorType))
            expect(next(l)).to(be_a(str))
