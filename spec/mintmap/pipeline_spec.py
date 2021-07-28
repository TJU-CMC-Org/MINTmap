import os
from datetime import datetime

from expects import *
from mamba import _it, context, describe, description, fit, it  # noqa: F401

from mintmap.pipeline import Pipeline

with describe(Pipeline) as self:
    with before.all:
        os.system("""rm -rf tmp/spec*""")
        config = {
            'custom_rpm':
                None,
            'input_file_path':
                'spec/support/input.fastq',
            'mapping_bundle_path':
                'spec/support',
            'prefix':
                'tmp/spec',
            'log_level':
                'debug',
            'execution_timestamp':
                datetime.now(),
            'execution_timestamp_str':
                '2021-01-21 15:54:18',
            'used_arguments_str':
                '...',
            'version':
                'v...',
            'fragments_lookup_table_path':
                'spec/support/LookupTable.tRFs.MINTmap_v1.txt',
            'fragments_type_table_path':
                'spec/support/OtherAnnotations.MINTmap_v1.txt',
            'trna_sequences_path':
                'spec/support/tRNAspace.Spliced.Sequences.MINTmap_v1.fa',
            'assembly':
                'GRCh37',
            'mapping_bundle_version':
                '1.0.0'
        }
        self.pipeline = Pipeline(config)

    with description('#initialize') as self:
        with it('sets files property'):
            expect(self.pipeline.files['exclusive']['expression']['txt']) \
                .to(equal(None))

    with description('#run') as self:
        with it('creates 6 output files'):
            self.pipeline.run()
            actual = int(os.popen('ls -1 tmp/spec-* | wc -l').read())
            expected = 6
            expect(actual).to(equal(expected))
