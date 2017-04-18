#! /usr/bin/perl
use strict;
use warnings;
use stefans_libs::root;
use Test::More tests => 2;
use stefans_libs::flexible_data_structures::data_table;

use FindBin;
my $plugin_path = "$FindBin::Bin";

my ( $value, @values, $exp, $p, $f, );

my $exec = $plugin_path . "/../bin/MINTmap.pl";
ok( -f $exec, 'the script has been found' );
my $outpath = "$plugin_path/data/output/MINTmap";
if ( -d $outpath ) {
	system("rm -Rf $outpath/*");
}else {
	system( "mkdir -p $outpath");
}

$p = $outpath."/out";
$f = "$plugin_path/data/exampleInput.fastq.gz";

ok ( -f $f, "Infile" );

my $cmd =
    "perl -I $plugin_path/../lib  $exec "
. " -p " . $p
. " -f " . $f
. " 1> /dev/null ";
my $start = time;
system( $cmd );
my $duration = time - $start;
print "Execution time: $duration s\n";
#print "\$exp = ".root->print_perl_var_def($value ).";\n";
