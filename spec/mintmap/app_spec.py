import os
import sys

from expects import *
from mamba import _it, context, describe, description, fit, it  # noqa: F401

from mintmap.app import App

with describe(App) as self:
    with description('.parse_arguments') as self:
        with context('when all arguments are set'):
            with it('parses arguments'):
                sys.argv = [
                    'mintmap',
                    'input_file',
                    '-c',
                    '1',
                    '-m',
                    'spec/support',
                    '-p',
                    'prefix_value',
                    '--log-level',
                    'warning'
                ]
                app = App()
                expect(app.prefix).to(equal('prefix_value'))
                expect(app.custom_rpm).to(equal(1))
                expect(os.path.exists(app.mapping_bundle_path)).to(be_true)
                expect(app.input_file_path).to(equal('input_file'))

        with context('when only mandatory arguments are set'):
            with it('parses arguments'):
                sys.argv = [
                    'mintmap',
                    'input_file',
                ]
                app = App()
                expect(app.prefix).to(equal('output'))
                expect(app.custom_rpm).to(equal(None))
                expect(os.path.exists(app.mapping_bundle_path)).to(be_true)
                expect(app.input_file_path).to(equal('input_file'))
