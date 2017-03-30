#! /usr/bin/perl
use strict;
use warnings;
use Test::More tests => 3;
BEGIN { use_ok 'MINTmap' }

use File::ShareDir;

use FindBin;
my $plugin_path = "$FindBin::Bin";

my ( $value, @values, $exp );
my $OBJ = MINTmap -> new({'debug' => 1});
is_deeply ( ref($OBJ) , 'MINTmap', 'simple test of function MINTmap -> new() ');

my $data_dir = $plugin_path;
$data_dir =~ s!/t/?$!/data/!;
$value = File::ShareDir::dist_file('MINTmap', "OtherAnnotations.MINTmap_v1.txt");
ok( -f $value , 'dist file OtherAnnotations.MINTmap_v1.txt access' );

#print "\$exp = ".root->print_perl_var_def($value ).";\n";
